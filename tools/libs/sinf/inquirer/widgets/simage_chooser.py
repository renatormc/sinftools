from PyQt5.QtWidgets import QWidget, QLabel, QToolButton, QFileDialog, QLineEdit, QGridLayout
from PyQt5.QtCore import QSize
from widgets.helpers import DataContext, get_template_type
from widgets.file_edit import FileEdit
import os

class SImageChooser(QWidget):
    has_data = True

    def __init__(self, config, config_all):
        QWidget.__init__(self)
        self.config = config
        self.has_caption = "caption" in self.config.keys()
        self.config_all = config_all
        self.setupUi()
        self.btt_choose.clicked.connect(self.choose)
        self.first_dir = os.getcwd()
        self.filter = "All Files (*)"
        self.led_adress.textChanged.connect(self.adressChange)
        

    def setupUi(self):
        if "min_width" in self.config.keys():
            size = self.minimumSize()
            size = QSize(config['min_width'], size.height())
            self.setMinimumSize(size)
            
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.led_adress = FileEdit(self)

        self.btt_choose = QToolButton()
        self.btt_choose.setText("...")

        if self.has_caption:
            label1 = QLabel("Arquivo")
            self.layout.addWidget(label1, 0, 0)
        self.layout.addWidget(self.led_adress, 0, 1)
        self.layout.addWidget(self.btt_choose, 0, 2)

        if self.has_caption:
            label2 = QLabel("Legenda")
            self.led_caption = QLineEdit()
            self.layout.addWidget(label2, 1, 0)
            self.layout.addWidget(self.led_caption, 1, 1)
            self.led_caption.setText(self.config['caption'])

    def choose(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file',
                                               self.first_dir, self.filter)
        if os.path.exists(filename[0]):
            self.led_adress.setText(filename[0])

    def get_data(self):
        text = self.led_adress.displayText()
        if text != '' and os.path.exists(text):
            caption = self.led_caption.displayText() if self.has_caption else ""
            template_type = get_template_type(self.config_all['template'])
            if template_type == 'xml':
                return {"path": text, "caption": caption}
            elif template_type == 'docx':
                return DataContext("image", {"path": text, "width": self.config['width'], "caption": caption})

    def get_data_json(self):
        return self.led_adress.displayText()

    def set_data_json(self, text):
        self.led_adress.setText(text)

    def clear_(self):
        self.led_adress.setText("")

    def adressChange(self, text):
        if os.path.exists(text):
            self.led_adress.setStyleSheet("color: rgb(0, 0, 0);")
        else:
            self.led_adress.setStyleSheet("color: rgb(255, 0, 0);")
