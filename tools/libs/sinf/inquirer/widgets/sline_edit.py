from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QSize
from widgets.helpers import convert


class SLineEdit(QLineEdit):
    has_data = True

    def __init__(self, config):
        QLineEdit.__init__(self)
        self.config = config
        if "mask" in config.keys():
            self.setInputMask(config['mask'])
        if "default" in config.keys():
            self.setText(config['default'])
        if "validator" in config.keys():
            rx = QRegExp(config['validator'])
            validator = QRegExpValidator(rx, self)
            self.setValidator(validator)
            self.textChanged.connect(self.textHasChanged)
        if "min_width" in config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)
        self.empty_content = self.displayText()

    def textHasChanged(self):
        if not self.hasAcceptableInput():
            self.setStyleSheet("QLineEdit { color: red;}")
        else:
            self.setStyleSheet("QLineEdit { color: black;}")

    def get_data(self):
        text = self.displayText()
        converted = convert(
            self.config['converter'], text) if "converter" in self.config.keys() else text
        if text != self.empty_content:
            return converted

    def get_data_json(self):
        return self.displayText()

    def set_data_json(self, text):
        self.setText(text)

    def mousePressEvent(self, e):
        if self.displayText() == self.empty_content:
            self.setCursorPosition(0)

    def clear_(self):
        if "default" in self.config.keys():
            self.setText(self.config['default'])
        else:
            self.setText("")
