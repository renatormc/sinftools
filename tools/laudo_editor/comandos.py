import win32com.client as win32
import os
from PyQt5 import QtCore, QtWidgets
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
sinftools_dir = os.getenv('SINFTOOLS')

word = win32.gencache.EnsureDispatch('Word.Application')
doc = word.ActiveDocument

class Janela(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.connections()
        self.setComandos()
        self.modo = "comando"
        

    def setupUI(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.lswComandos = QtWidgets.QListWidget()
        main_layout.addWidget(self.lswComandos)
        self.setLayout(main_layout)
        self.setGeometry(250,200, 300, 400)
        
    def setComandos(self):
        self.comandos ={
            "editar_modelo": self.editar_modelo,
            "editar_modelo_inserir": self.editar_modelo_inserir
        }
        for key in self.comandos:
            self.lswComandos.addItem(key)

    def connections(self):
        self.lswComandos.itemDoubleClicked.connect(self.double_click)
    
    def double_click(self, item):
        self.comandos[item.text()]()

    ####comandos##############
    def editar_modelo(self):
        self.lswComandos.clear()
        for item in os.listdir(f"{sinftools_dir}\\var\\Modelos"):
            if os.path.isfile(f"{sinftools_dir}\\var\\Modelos\\{}".format(item)):
                self.lswComandos.addItem(item)
        try:
            self.lswComandos.itemDoubleClicked.disconnect(self.double_click)   
        except:
            pass 
        self.lswComandos.itemDoubleClicked.connect(self.abrir_modelo)
        self.modo = "modelo"

    def editar_modelo_inserir(self):
        self.lswComandos.clear()
        for item in os.listdir(f"{sinftools_dir}\\var\\Modelos\\Modelos"):
            self.lswComandos.addItem(item)
        try:
            self.lswComandos.itemDoubleClicked.disconnect(self.double_click)   
        except:
            pass 
        self.lswComandos.itemDoubleClicked.connect(self.abrir_modelo)
        self.modo = "modelo_inserir"
        
    ##########################

    def abrir_modelo(self, item):
        if self.modo == "modelo_inserir":
            word.Documents.Open(f"{sinftools_dir}\\var\\Modelos\\Modelos\\{item.text()}")
        elif self.modo == "modelo":
            word.Documents.Open(f"{sinftools_dir}\\var\\Modelos\\{item.text()}")
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    janela = Janela()
    janela.show()
    sys.exit(app.exec_())