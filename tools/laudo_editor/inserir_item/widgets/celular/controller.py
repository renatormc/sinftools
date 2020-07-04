import os
from PyQt5.QtWidgets import QWidget, QFileDialog
from .view import Ui_Form
script_dir = os.path.dirname(os.path.realpath(__file__))
from ..components.lib.helpers import ImageSet

class Celular(QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.connections()
        self.dir_imagens = 'C:\\'

    def setWordHandler(self, wh):
        self.wh = wh 

    def connections(self):
        self.ui.btnFotoCelular.clicked.connect(self.selecionar_foto_celular)
        self.ui.btnFotoEtiqueta.clicked.connect(self.selecionar_foto_etiqueta)
        self.ui.btnFotoDispositivos.clicked.connect(self.selecionar_foto_dispositivos)

    def inserir_word(self):
        self.wh.setTemplate(script_dir + "\\template.docx")
        context = {
            "marca": self.ui.marcaLineEdit.displayText(),
            "modelo": self.ui.modeloLineEdit.displayText(), 
            "imei": self.ui.imeiLineEdit.displayText(), 
            "seq_chip1": self.ui.sequenciaChip1LineEdit.displayText(),
            "marca_bateria": self.ui.marcaBateriaLineEdit.displayText(),
            "operadora_chip1": self.ui.operadoraChip1LineEdit.displayText(),
            "seq_chip2": self.ui.sequenciaChip2LineEdit.displayText(),
            "operadora_chip2": self.ui.operadoraChip2LineEdit.displayText(),
            "marca_sd": self.ui.marcaSDLineEdit.displayText(),
            "capacidade_sd": self.ui.capacidadeSDLineEdit.displayText(),
            "legenda_dispositivos": self.ui.legendaDispositivosLineEdit.displayText(),
            "nome_objeto": self.ui.nomeObjetoLineEdit.displayText(),
            }
        ims = ImageSet()
        ims.addImage(tag="foto_celular", path=self.ui.lineEditFotoCelular.displayText(), width=50)
        ims.addImage(tag="foto_etiqueta", path=self.ui.lineEditFotoEtiqueta.displayText(), width=50)
        ims.addImage(tag="foto_dispositivos", path=self.ui.lineEditFotoDispositivos.displayText(), width=50)
        self.wh.insert(context, imagens=ims.getImages())
      
    def selecionar_foto_celular(self):
        nome = QFileDialog.getOpenFileName(self, 'Open file', self.dir_imagens,"Image files (*.jpg *.gif)")
        self.ui.lineEditFotoCelular.setText(nome[0])
        self.dir_imagens = os.path.dirname(nome[0])
    
    def selecionar_foto_etiqueta(self):
        nome = QFileDialog.getOpenFileName(self, 'Open file', self.dir_imagens,"Image files (*.jpg *.gif)")
        self.ui.lineEditFotoEtiqueta.setText(nome[0])
        self.dir_imagens = os.path.dirname(nome[0])
    
    def selecionar_foto_dispositivos(self):
        nome = QFileDialog.getOpenFileName(self, 'Open file', self.dir_imagens,"Image files (*.jpg *.gif)")
        self.ui.lineEditFotoDispositivos.setText(nome[0])
        self.dir_imagens = os.path.dirname(nome[0])

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = Celular()
    ex.show()
    sys.exit(app.exec_())