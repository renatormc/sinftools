from .ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from .obj_pics import ObjPics
from helpers import get_objects_from_pics, gen_laudo
from pathlib import Path
import config
import json


class MainWindow(QMainWindow):
    def __init__(self, folder="."):
        super(self.__class__, self).__init__()
        self.folder = Path(folder)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.load_pics()
        self.load_last_context()

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

    def save(self, context):
        path = self.folder / ".last_context.json"
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(context, ensure_ascii=False, indent=4))

    def load_last_context(self):
        path = self.folder / ".last_context.json"
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.ui.ledPericia.setText(data['pericia'])
            self.ui.ledRequisitante.setText(data['requisitante'])
            self.ui.ledProcedimento.setText(data['procedimento'])
            self.ui.ledDataExame.setText(data['data_exame'])
            self.ui.ledDataEntrada.setText(data['data_entrada'])
            self.ui.ledOcorrenciaOdin.setText(data['ocorrencia_odin'])
            self.ui.ledDataOcorrencia.setText(data['data_ocorrencia'])
            self.ui.ledAutoridade.setText(data['autoridade'])
            self.ui.ledRevisor.setText(data['revisor'])

    def ok(self):
        context = {
            'pericia': self.ui.ledPericia.displayText(),
            'requisitante': self.ui.ledRequisitante.displayText(),
            'procedimento': self.ui.ledProcedimento.displayText(),
            'data_exame': self.ui.ledDataExame.displayText(),
            'data_entrada': self.ui.ledDataEntrada.displayText(),
            'ocorrencia_odin': self.ui.ledOcorrenciaOdin.displayText(),
            'data_ocorrencia': self.ui.ledDataOcorrencia.displayText(),
            'autoridade': self.ui.ledAutoridade.displayText(),
            'revisor': self.ui.ledRevisor.displayText(),
            'objects': []
        }
        for obj in self.objects:
            data = obj.get_data()
            context['objects'].append(data)

        path = config.sinftools_dir / "var/config/local_context.json"
        if not path.exists():
            path.write_text("{\n}", encoding="utf-8")
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        context.update(data)
        self.save(context)
        gen_laudo(context, str(self.folder / "laudo"))
        print("Laudo gerado")
        self.close()
