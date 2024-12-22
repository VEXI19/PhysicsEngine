from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QStackedWidget, QMainWindow
from PyQt5.QtCore import Qt
from ..Widgets.folder_picker import FolderPicker
from ..Widgets.file_picker import FilePicker

class VisualizationPickView(QWidget):
    """
    This view is used to pick simulation directory and file. It manages navigation between directory picker and file picker.
    """
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.current_simulation_directory: str | None = None

        # Layouts
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.navigation_layout = QHBoxLayout()
        self.navigation_layout.setContentsMargins(5, 5, 5, 5)
        self.navigation_layout.setAlignment(Qt.AlignHCenter)

        # Widgets
        self.pick_stack = QStackedWidget()
        self.directory_picker = FolderPicker(self)
        self.file_picker = FilePicker(self)

        self.pick_stack.addWidget(self.directory_picker)
        self.pick_stack.addWidget(self.file_picker)
        self.pick_stack.setCurrentWidget(self.directory_picker)

        # Navigation buttons
        self.navigation_button_back = QPushButton("Back")
        self.navigation_button_back.setObjectName("small_button")
        self.navigation_button_back.setDisabled(True)
        self.navigation_button_back.clicked.connect(lambda: self.navigate(False))
        self.navigation_button_back.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.navigation_button_forward = QPushButton("Forward")
        self.navigation_button_forward.setObjectName("small_button")
        self.navigation_button_forward.setDisabled(True)
        self.navigation_button_forward.clicked.connect(lambda: self.navigate())
        self.navigation_button_forward.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.navigation_layout.addWidget(self.navigation_button_back)
        self.navigation_layout.addWidget(self.navigation_button_forward)

        self.title = QLabel("Visualization")
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setObjectName("title")

        # Add widgets
        self.layout.addWidget(self.title)
        self.layout.addLayout(self.navigation_layout)
        self.layout.addWidget(self.pick_stack)

    def refresh_navigation(self) -> None:
        """
        Refreshes navigation buttons. Disables back button if current index is 0, disables forward button
        if current index is 1 or current simulation directory is None.
        """

        if self.pick_stack.currentIndex() == 0:
            self.navigation_button_back.setDisabled(True)
        else:
            self.navigation_button_back.setDisabled(False)

        if self.pick_stack.currentIndex() == 1 or self.current_simulation_directory is None:
            self.navigation_button_forward.setDisabled(True)
        else:
            self.navigation_button_forward.setDisabled(False)

    def navigate(self, forward: bool = True):
        """
        Navigates between widgets in the view. If forward is True, navigates to the next widget, otherwise navigates to
        the previous one.

        Args:
            forward (bool): flag to navigate forward or backward
        """

        current_index = self.pick_stack.currentIndex()
        if forward:
            self.pick_stack.setCurrentIndex(current_index + 1)
        else:
            self.pick_stack.setCurrentIndex(current_index - 1)
        self.refresh_navigation()
        self.pick_stack.currentWidget().populate_view()
