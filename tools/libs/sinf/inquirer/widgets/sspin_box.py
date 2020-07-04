from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtCore import QSize


class SSpinBox(QSpinBox):
    has_data = True

    def __init__(self, config):
        QSpinBox.__init__(self)
        self.config = config
        if "default" in config.keys():
            self.setValue(config['default'])
        else:
            self.setValue(1)
        if "min" in config.keys():
            self.setMinimum(config['min'])
        if "max" in config.keys():
            self.setMaximum(config['max'])
        if "min_width" in config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)
        

    def textHasChanged(self):
        if not self.hasAcceptableInput():
            self.setStyleSheet("QLineEdit { color: red;}")
        else:
            self.setStyleSheet("QLineEdit { color: black;}")

    def get_data(self):
        return self.value()

    def get_data_json(self):
        return self.value()

    def set_data_json(self, value):
        self.setValue(value)

    def clear_(self):
        if "default" in self.config.keys():
            self.setValue(self.config['default'])
    
