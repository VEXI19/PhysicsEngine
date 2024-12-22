from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
import os

from PhysicsEngine.Config.Config import Config


class FolderPicker(QWidget):
    """
    QWidget class for folder picker. This widget is used to pick a folder containing simulation files.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.config = Config()

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Placeholder for dynamic buttons
        self.folder_buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.folder_buttons_layout)

        self.no_directory_label = QLabel("")
        self.no_directory_label.setObjectName("error")
        self.layout.addWidget(self.no_directory_label)

        self.folder_path = self.config["SIMULATION"]["simulation_files_folder_path"]
        self.populate_view()

    def populate_view(self) -> None:
        """
        Populates the view with simulation folders.

        If no folders are found, displays an error message.

        If a button is clicked, sets the current simulation directory in the parent object and navigates to the next view.
        """
        # Clear existing buttons
        while self.folder_buttons_layout.count():
            widget = self.folder_buttons_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        if not os.path.isdir(self.folder_path):
            self.no_directory_label.setText(f"Selected folder does not exist: {self.folder_path}")
        else:
            # Display subfolders as buttons
            subfolders = [f.path for f in os.scandir(self.folder_path) if f.is_dir()]
            if not subfolders:
                self.no_directory_label.setText(f"No subfolders found in: {self.folder_path}")
            else:
                for subfolder in subfolders:
                    folder_name = os.path.basename(subfolder)
                    button = QPushButton(folder_name)
                    button.setObjectName("big_button")
                    button.clicked.connect(lambda _, path=subfolder: self.folder_selected(path))
                    self.folder_buttons_layout.addWidget(button)

    def folder_selected(self, path: str) -> None:
        """
        Sets the current simulation directory in the parent object and navigates to the next view.

        Args:
            path (str): path to the selected folder
        """
        if self.parent:
            self.parent.current_simulation_directory = path
            self.parent.navigate()
