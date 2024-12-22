import os

from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
import sys
from PhysicsEngine.UI.Widgets.menu_bar import MenuBar
from PhysicsEngine.UI.Views.picker import VisualizationPickView


class MainWindow(QMainWindow):
    """
    Main window class for the application. Connects all the views and widgets.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("JD Physics Engine")
        self.setWindowState(Qt.WindowMaximized)

        # Menubar
        self.menuBar = MenuBar(self)

        # Status Bar
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready")

        margin = 10
        self.visualization_view = VisualizationPickView(self)
        self.visualization_view.setContentsMargins(margin, margin, margin, margin)
        self.setCentralWidget(self.visualization_view)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handles key press events.

        Args:
            event (QKeyEvent): Key press event
        """

        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            sys.exit(0)
