import os
from PyQt5.QtWidgets import QWidget, QFileDialog
from .view import Ui_Form
script_dir = os.path.dirname(os.path.realpath(__file__))

class Computador(QWidget):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.connections()
        self.dir_imagens = 'C:\\'

    def setWordHandler(self, wh):
        self.wh = wh 

    def connections(self):
        pass

    def inserir_word(self):
        self.wh.setTemplate(script_dir + "\\template.docx")
        context = {
           
            }
        # ims = ImageSet()
        # ims.addImage(tag="foto_celular", path=self.ui.lineEditFotoCelular.displayText(), width=50)
        # self.wh.insert(context, imagens=ims.getImages())
        self.wh.insert(context)