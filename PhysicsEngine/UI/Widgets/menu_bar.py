from PyQt5.QtWidgets import QMenu, QAction, QFileDialog, QMessageBox, QMainWindow
from typing import Callable
import sys

from PhysicsEngine.Config.Config import Config


class MenuBar:
    def __init__(self, window: QMainWindow):
        self.window = window
        self.menubar = window.menuBar()
        self.config = Config()

        # Top-level menus
        file_menu = self.menubar.addMenu("File")
        edit_menu = self.menubar.addMenu("Edit")
        options_menu = self.menubar.addMenu("Options")
        help_menu = self.menubar.addMenu("Help")

        # File Menu
        self._add_action(file_menu, "New", "Ctrl+N", True)
        file_menu.addSeparator()
        self._add_action(file_menu, "Exit", "Ctrl+Q", trigger=lambda: sys.exit(0))

        # Edit Menu
        self._add_action(edit_menu, "Select all", "Ctrl+A", trigger=lambda: print("Select all"))
        self._add_action(edit_menu, "Copy", "Ctrl+C", trigger=lambda: print("Copy"))
        self._add_action(edit_menu, "Paste", "Ctrl+V", trigger=lambda: print("Paste"))
        self._add_action(edit_menu, "Cut", "Ctrl+X", trigger=lambda: print("Cut"))

        # Options Menu
        self._add_action(options_menu, "Preferences", "Ctrl+P", True)
        self._add_action(options_menu, "Choose simulations path", trigger=self.simulations_path_trigger)

        # Help Menu
        self._add_action(help_menu, "About", trigger=self._about_trigger)

    def _add_action(self, menu: QMenu, text: str, shortcut: str = "", disabled: bool = False, trigger: Callable = None) -> QAction:
        action = menu.addAction(text)
        action.setShortcut(shortcut)
        action.setDisabled(disabled)
        if trigger:
            action.triggered.connect(trigger)
        return action

    def _about_trigger(self):
        QMessageBox.about(self.menubar, "About", "This is a sample application.")

    def simulations_path_trigger(self):
        file_path = QFileDialog.getExistingDirectory(options=QFileDialog.Options())
        if file_path:
            self.config.set_value("UI", "simulation_files_folder_path", file_path)
