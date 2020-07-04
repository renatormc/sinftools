from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

class Spacer(QSpacerItem):
    has_data = False

    def __init__(self):
        super(QSpacerItem, self).__init__(150, 10, QSizePolicy.Expanding)

    def get_data(self):
        pass

    def get_data_json(self):
        pass

    def set_data_json(self, text):
        pass

    def clear_(self):
        pass