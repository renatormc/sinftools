from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QSize

class STextEdit(QTextEdit):
    has_data = True

    def __init__(self, config):
        QTextEdit.__init__(self)
        self.config = config
        if "default" in config.keys():
            self.setText(config['default'])
        if "min_width" in config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)
        self.empty_content = self.toPlainText()

    def get_data(self):
        text = self.toPlainText()
        if text != self.empty_content:
            return text

    def get_data_json(self):
        return self.toPlainText()

    def set_data_json(self, text):
        self.setText(text)

    def clear_(self):
        if "default" in self.config.keys():
            self.setText(self.config['default'])
        else:
            self.setText("")