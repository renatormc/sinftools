from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import QSize
from widgets.simage_chooser import SImageChooser
from widgets.helpers import DataContext


class SImageGroup(QWidget):
    has_data = True

    def __init__(self, config, config_all):
        QWidget.__init__(self)
        self.config = config
        self.config_all = config_all
        self.setupUi()

    def setupUi(self):
        if "min_width" in self.config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.items = []
        for i, item in enumerate(self.config['items']):
            w = SImageChooser(item, self.config_all)
            self.items.append(w)
            label = QLabel(item['label'])
            self.layout.addWidget(label, i, 0)
            self.layout.addWidget(w, i, 1)


    def clear_(self):
        for item in self.items:
            item.clear_()

    def get_data_json(self):
        return [item.get_data_json() for item in self.items]

    def set_data_json(self, data):
        try:
            for i, item_data in enumerate(data):
                self.items[i].set_data_json(item_data)
        except:
            pass


    def get_data(self):
        data = []
        for item in self.items:
            item_context = item.get_data()
            if item_context is not None:
                data.append(item_context.data)
        return DataContext("image_group", {"per_row": self.config["per_row"], "images": data})