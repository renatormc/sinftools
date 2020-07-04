
from PyQt5.QtWidgets import QHBoxLayout, QComboBox
from PyQt5.QtCore import QSize
from widgets.sline_edit import SLineEdit
import json
from copy import deepcopy

class SCatEdit(QHBoxLayout):
    has_data = True

    def __init__(self, config):
        QHBoxLayout.__init__(self)
        self.config = config
        self.setupUi()
        if "min_width" in config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.edit.setMinimumSize(size)
        
    def setupUi(self):
        default = None
        if "default" in self.config.keys():
            default = deepcopy(self.config['default'])
            del self.config['default']
        self.edit = SLineEdit(self.config)
        self.addWidget(self.edit, 1)
        self.combo = QComboBox()
        if default:
            self.set_data_json(default)
        self.addWidget(self.combo, 0)

    # def setMinimumSize(self, width):
    #     size = self.minimumSize()
    #     size = QSize(self.config['min_width'], size.height())
    #     self.edit.setMinimumSize(size)
       


    def get_data(self):
        return {
            'value': self.edit.get_data(),
            'category': self.combo.currentText()
        }
              

    def get_data_json(self):
        return {
            'value': self.edit.displayText(),
            'category': self.combo.currentText()
        }

    def set_data_json(self, data):
       
        index = self.combo.findText(data['category'])
        if index:
            self.combo.setCurrentIndex(index)
        self.edit.setText(data['value'])
       

    def clear_(self):
        self.edit.clear_()