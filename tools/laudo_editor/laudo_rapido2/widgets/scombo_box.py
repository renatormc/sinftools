
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QSize


class SComboBox(QComboBox):
    has_data = True

    def __init__(self, config):
        QComboBox.__init__(self)
        self.config = config
        if not 'allow_null' in config.keys() or config['allow_null']:
            self.addItem("----")
        if "editable" in config.keys() and config['editable'] == True:
            self.setEditable(True)
        if "min_width" in config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)

    def add_item(self, item):
        if isinstance(item, str):
            self.addItem(item, item)
        elif isinstance(item, dict):
            self.addItem(item['label'], item['data'])

    def update_default(self):
        if "default" in self.config.keys():
            index = self.findText(self.config['default'])
        else:
            index = self.findText("----")
        if index:
            self.setCurrentIndex(index)

    def get_data(self):
        index = self.currentIndex()
        text = self.currentText()
        if text != '----':
            return self.itemData(index)

    def get_data_json(self):
        return self.currentText()

    def set_data_json(self, text):
        index = self.findText(text.strip())
        if index:
            self.setCurrentIndex(index)

    def clear_(self):
        self.update_default()
