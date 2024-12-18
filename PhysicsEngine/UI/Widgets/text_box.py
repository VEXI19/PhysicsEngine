from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5 import QtCore


class TextBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        margin = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(margin, margin, margin, margin)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.text_widgets: dict = {}

    def add_text_widget(self, name: str, text: str):
        text_widget = QLabel(text)
        text_widget.setText(text)
        self.text_widgets[name] = text_widget
        self.layout.addWidget(text_widget)

    def update_widget(self, name: str, text: str):
        text_widget = self.text_widgets[name]
        text_widget.setText(text)

    def update_multiple_widgets(self, text_widgets: dict):
        for name, text_widget in text_widgets.items():
            if name in self.text_widgets.keys():
                self.update_widget(name, text_widget)