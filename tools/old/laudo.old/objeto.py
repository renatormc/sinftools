from ui_objeto import Ui_Objeto
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path

class Objeto(QWidget):
    def __init__(self, file: Path):
        super(self.__class__, self).__init__()
        self.ui = Ui_Objeto()
        self.ui.setupUi(self)
        self.connections()
        self.ui.led_legenda.setText(file.name)
        self.ui.led_objeto.setText(file.name)
        self.add_pic(file)
        # for i in range(10):

    def add_pic(self, file: Path):
        w = 300
        h = 300
        pixmap = QPixmap(str(file)).scaled(w, h, Qt.KeepAspectRatio)
        self.ui.lblImage.setPixmap(pixmap)
        self.ui.lblImage.setFixedWidth(w)


    def connections(self):
        pass
