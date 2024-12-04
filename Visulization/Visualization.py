import sys
from .Gui import Gui
from PyQt5 import QtWidgets


def start(file: str):
    app = QtWidgets.QApplication(sys.argv)
    gui = Gui(file)
    gui.showMaximized()  # Maximized mode
    sys.exit(app.exec_())
