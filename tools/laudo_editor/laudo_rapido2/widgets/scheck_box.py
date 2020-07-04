from PyQt5.QtWidgets import QCheckBox

class SCheckBox(QCheckBox):
    has_data = True

    def __init__(self, config):
        QCheckBox.__init__(self)
        self.config = config
        if 'label' in config.keys():
            self.setText(config['label'])
        self.clear_()

    def get_data(self):
        return self.isChecked()
      
    def get_data_json(self):
        return self.isChecked()
       
    def set_data_json(self, value):
        self.setChecked(value)

    def clear_(self):
        if "default" in self.config.keys():
            self.setChecked(self.config['default'])