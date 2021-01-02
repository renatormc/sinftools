from .ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from .obj_pics import ObjPics
from helpers import get_objects_from_pics, gen_laudo
from pathlib import Path


class MainWindow(QMainWindow):
    def __init__(self, folder="."):
        super(self.__class__, self).__init__()
        self.folder = Path(folder)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.load_pics()

    def load_pics(self):
        self.objects = []
        objects = get_objects_from_pics(str(self.folder / "fotos"))
        for obj in objects:
            objPics = ObjPics(obj)
            self.ui.layPics.addWidget(objPics)
            self.objects.append(objPics)

    def connections(self):
        self.ui.btnOk.clicked.connect(self.ok)
        self.ui.btnCancel.clicked.connect(self.cancel)

    def cancel(self):
        self.close()

    def ok(self):
        context = {
            'pericia': self.ui.ledPericia.displayText(),
            'requisitante': self.ui.ledRequisitante.displayText(),
            'procedimento': self.ui.ledProcedimento.displayText(),
            'data_exame': self.ui.ledDataExame.displayText(),
            'data_entrada': self.ui.ledDataEntrada.displayText(),
            'objects': []
        }
        for obj in self.objects:
            data = obj.get_data()
            context['objects'].append(data)
        gen_laudo(context, str(self.folder / "laudo"))
