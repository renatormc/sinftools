from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
import piexif
import os
import config

class ObjPics(QWidget):
    def __init__(self, obj):
        super(self.__class__, self).__init__()
        self.obj = obj
        self.setupUi()
        

    def setupUi(self):
        self.lblCaption = QLabel(self.obj['report_name'])
        self.layMain = QVBoxLayout()
        self.layMain.addWidget(self.lblCaption)
        self.setLayout(self.layMain)

        self.cbxType = QComboBox()
        for t in config.object_types:
            self.cbxType.addItem(t)
        self.layMain.addWidget(self.cbxType)

        self.lswPics = QListWidget()
        self.lswPics.setDragDropMode(QAbstractItemView.InternalMove)
        self.lswPics.setSelectionMode(QAbstractItemView.SingleSelection)
        self.lswPics.setSpacing(10)
        self.lswPics.setIconSize(QSize(100, 100))
        self.lswPics.setResizeMode(QListView.Adjust)
        for pic in self.obj['pics']:
            exif_dict = piexif.load(pic)
            thumbnail = exif_dict.pop("thumbnail")
            if thumbnail is not None:
                pix1 = QPixmap()
                pix1.loadFromData(thumbnail,"JPG")
                item = QListWidgetItem(QIcon(pix1.scaled(100,100,  Qt.KeepAspectRatio, Qt.SmoothTransformation)), os.path.split(pic)[-1])
                item.setData(Qt.UserRole, pic)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Checked)
                self.lswPics.addItem(item)
        self.layMain.addWidget(self.lswPics)

    def get_data(self):
        data = {
            'name': self.lblCaption.text(),
            'type': self.cbxType.currentText(),
            'pics': []
        }
        for i in range(self.lswPics.count()):
            item = self.lswPics.item(i)
            if item.checkState() == Qt.Checked:
                data['pics'].append(item.data(Qt.UserRole))
        return data
                
           
            
        