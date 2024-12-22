from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5 import QtCore


class TextBox(QWidget):
    """
    TextBox class is a custom QWidget class that displays text in a vertical layout.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        margin = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(margin, margin, margin, margin)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)

        self.text_widgets: dict = {}

    def add_text_widget(self, name: str, text: str):
        """
        Adds a text widget to the layout.

        Args:
            name (str): name of the text widget, used to save widget in dictionary
            text (str): text to display
        """

        text_widget = QLabel(text)
        text_widget.setText(text)
        self.text_widgets[name] = text_widget
        self.layout.addWidget(text_widget)

    def update_widget(self, name: str, text: str) -> None:
        """
        Updates the text of a text widget.

        Args:
            name (str): name of the text widget
            text (str): text to display
        """

        text_widget = self.text_widgets[name]
        text_widget.setText(text)

    def update_multiple_widgets(self, text_widgets: dict) -> None:
        """
        Updates multiple text widgets.

        Args:
            text_widgets (dict): dictionary of text widgets to update
        """

        for name, text_widget in text_widgets.items():
            if name in self.text_widgets.keys():
                self.update_widget(name, text_widget)
