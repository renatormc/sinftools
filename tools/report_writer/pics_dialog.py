from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pathlib import Path
import re


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class Objeto(QWidget):
    def __init__(self, name, pics, number):
        super(self.__class__, self).__init__()
        self.name = name
        self.pics = pics
        self.number = number
        self.pics_items = []
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        h_layout = QHBoxLayout()
        label = QLabel("Nome: ")
        h_layout.addWidget(label)
        self.led_name = QLineEdit()
        title = f"Evidência {self.number}"
        self.led_name.setText(title)
        h_layout.addWidget(self.led_name)
        self.main_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        label = QLabel("Tipo: ")
        h_layout.addWidget(label)
        self.cbx_tipo = QComboBox()
        items = ['Celular', 'Notebook', 'Chip', 'Computador', 'Tablet']
        items.sort()
        for item in items:
            self.cbx_tipo.addItem(item)
        h_layout.addWidget(self.cbx_tipo)
        self.main_layout.addLayout(h_layout)

        layout = QHBoxLayout()
        for pic in self.pics:
            item_pic = {}
            layout_pic = QVBoxLayout()
            label = QLabel()
            pixmap = QPixmap(pic).scaledToWidth(200)
            label.setPixmap(pixmap)
            layout_pic.addWidget(label)
            item_pic['led_caption'] = QLineEdit()
            item_pic['led_caption'].setText(title)
            layout_pic.addWidget(item_pic['led_caption'])
            item_pic['file'] = pic
            layout.addLayout(layout_pic)
            self.pics_items.append(item_pic)
        self.main_layout.addLayout(layout)

    def get_data(self):
        ret = {
            'name': self.led_name.displayText(), 
            'type': self.cbx_tipo.currentText(),
            'pics': []
        }
        for pic in self.pics_items:
            ret['pics'].append({
                'file': pic['file'],
                'caption': pic['led_caption'].displayText()
            })
        return ret


class PicsDialog(QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.widgets = []
        self.setup_ui()

    def setup_ui(self):
        self.items = []
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        objects = self.get_pics()
        for key, value in objects.items():
            w = Objeto(key, value['pics'], value['number'])
            self.main_layout.addWidget(w)
            self.widgets.append(w)
            self.main_layout.addWidget(QHLine())

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(self.button_box)

    # def accept(self):
    #     pass

    # def reject(self):
    #     pass

    def get_pics(self):
        folder = Path("./fotos")
        objects = {}
        reg = re.compile(r'((^[A-Za-z]+)(\d+)).*')
        for entry in folder.iterdir():
           
            if not entry.is_file() or not entry.suffix.lower()  in ['.jpg', '.png']:
                continue
            res = reg.search(entry.name)
            obj = res.group(1).upper()
            try:
                objects[obj]['pics'].append(str(entry))
            except KeyError:
                objects[obj] = {'number': int(
                    res.group(3)), 'pics': [str(entry)]}
                # objects.sort(key=lambda x: x['number'])
        return objects
        

    def get_data(self):
        return [w.get_data() for w in self.widgets]
