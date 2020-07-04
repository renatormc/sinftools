
from PyQt5.QtWidgets import QHBoxLayout, QComboBox
from PyQt5.QtCore import QSize
from widgets.sline_edit import SLineEdit
import json

class SCatEdit(QHBoxLayout):
    has_data = True

    def __init__(self, config):
        QHBoxLayout.__init__(self)
        self.config = config
        self.setupUi()
        if "default" in config.keys():
            self.edit.setText(config['default'])
        if "min_width" in config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)
        
    def setupUi(self):
        self.edit = SLineEdit(self.config)
        self.addWidget(self.edit, 1)
        self.combo = QComboBox()
        self.addWidget(self.combo, 0)


    def get_data(self):
        return {
            'value': self.edit.get_data(),
            'category': self.combo.currentText()
        }
              

    def get_data_json(self):
        return {
            'edit_text': self.edit.displayText(),
            'combo_text': self.combo.currentText()
        }

    def set_data_json(self, data):
        index = self.combo.findText(data['combo_text'])
        if index:
            self.combo.setCurrentIndex(index)
        self.edit.setText(data['edit_text'])
       

    def clear_(self):
        self.edit.clear_()