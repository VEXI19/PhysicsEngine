from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PhysicsEngine import MainWindow
import qdarkstyle
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))
    main_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    with open("./PhysicsEngine/UI/Styles/style.qss", "r") as file:
        app.setStyleSheet(main_stylesheet + file.read())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
