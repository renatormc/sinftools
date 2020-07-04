import os
import MainInterface
from PyQt5 import QtCore, QtWidgets
import sys
import codecs
import json
import shutil


scriptDir = os.path.dirname(os.path.realpath(__file__))
with codecs.open(os.path.abspath(os.path.dirname(__file__)) + "\\..\\config.json",'r',encoding="utf-8") as arq:
            config = json.load(arq)

def copyanything(src, dst):   
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

class Ui_MainWindow(MainInterface.Ui_MainWindow):
    def __init__(self, main):
        self.main = main
        self.setupUi(main)
        self.connections()
        with codecs.open(os.path.abspath(os.path.dirname(__file__)) + "\\..\\config.json",'r',encoding="utf-8") as arq:
            self.config = json.load(arq)
        self.popular_lista()

    def popular_lista(self):
        for entry in os.listdir(self.config['pasta_modelos']):
            if entry.endswith('.docx'):
                self.lsw_modelos.addItem(entry)

    def connections(self):
        self.btn_ok.clicked.connect(self.ok_click)

    def ok_click(self):
        nome_caso, ok1 = QtWidgets.QInputDialog.getText(self.btn_ok,'Novo caso','Nome do caso:')
        if ok1:
            if len(sys.argv)> 1: #verifica se o diretorio foi passado pela linha de comando
                diretorio_destino, ok2 = sys.argv[1], True 
            else:
                diretorio_destino, ok2 = QtWidgets.QInputDialog.getText(self.btn_ok,'Diretorio de destino','Diretório de destino:')
            if ok2:
                #copiar template de pastas
                copyanything(self.config['template_novo_laudo'],diretorio_destino + '\\' +  nome_caso)

                #copiar modelo de laudo
                modelo = self.config['pasta_modelos'] + '\\' +self.lsw_modelos.currentItem().text()
                shutil.copyfile(modelo, diretorio_destino + '\\' +  nome_caso + '\\' + nome_caso + '.docx')
                sys.exit()
               

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.setWindowTitle("Novo caso")
MainWindow.show()
sys.exit(app.exec_())
