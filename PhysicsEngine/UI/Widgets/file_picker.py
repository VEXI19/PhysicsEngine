from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
import os
from PhysicsEngine.UI.Windows.simulation_window import SimulationWindow

class FilePicker(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.simulation_windows = []

        # Layout setup
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.no_directory_label = QLabel()
        self.no_directory_label.setObjectName("error")
        self.layout.addWidget(self.no_directory_label)

        # Placeholder for dynamic buttons
        self.file_buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.file_buttons_layout)

    def populate_view(self):
        folder_path = os.path.join(self.parent.current_simulation_directory, "Simulations")
        self.no_directory_label.setText("")

        # Clear existing buttons
        while self.file_buttons_layout.count():
            widget = self.file_buttons_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Display files as buttons
        files = [f.path for f in os.scandir(folder_path) if f.is_file()]
        if not files:
            self.no_directory_label.setText(f"No files found in: {folder_path}")
        else:
            for file_path in files:
                file_name = os.path.basename(file_path)
                button = QPushButton(file_name)
                button.setObjectName("big_button")
                button.clicked.connect(lambda _, path=file_path: self.file_selected(path))
                self.file_buttons_layout.addWidget(button)

    def file_selected(self, path):
        print(f"File selected: {path}")
        sim_window = SimulationWindow(path)
        sim_window.show()
        self.simulation_windows.append(sim_window)
