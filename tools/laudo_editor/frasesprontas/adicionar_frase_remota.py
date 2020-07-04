from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys
from remote import Remote
import win32com.client as win32
import json
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUI()
        self.connections()
        self.remote = Remote()
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        # self.word = win32.Dispatch('Word.Application')
        self.doc = self.word.ActiveDocument


    def setupUI(self):
        self.setWindowIcon(QtGui.QIcon('{}\\resources\\icon.png'.format(script_dir)))
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

        self.layout1 = QHBoxLayout()
        self.edt_trecho = QLineEdit()
        self.layout1.addWidget(self.edt_trecho)
        self.btn_pesquisar = QPushButton("Pesquisar")
        self.layout1.addWidget(self.btn_pesquisar)
        self.main_layout.addLayout(self.layout1)

        self.lsw_lista = QListWidget()
        self.lsw_lista.setStyleSheet("alternate-background-color: #b5e7a0;background-color: white;")
        self.lsw_lista.setAlternatingRowColors(True)
        self.lsw_lista.setTextElideMode(QtCore.Qt.ElideNone)
        self.lsw_lista.setWordWrap(True)
        self.main_layout.addWidget(self.lsw_lista)

    def connections(self):
        self.btn_pesquisar.clicked.connect(self.pesquisar)
        self.lsw_lista.itemDoubleClicked.connect(self.itemClicked)
        self.edt_trecho.returnPressed.connect(self.pesquisar)

    def pesquisar(self):
        self.resultados = []
        termo = self.edt_trecho.displayText()
        result = self.remote.getFrases(termo)
        if result:
            frases = json.loads(result)
            self.lsw_lista.clear()
        for frase in frases:
            texto = frase['texto']
            if len(texto) > 500:
                texto = texto[:500] + "..."
            self.lsw_lista.addItem(texto)
            self.resultados.append(frase['id'])

    def itemClicked(self, item):
        frase = self.remote.getFrase(self.resultados[self.lsw_lista.currentRow()])
        self.word.Selection.TypeText(frase)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setGeometry(500,300,800,600)
    w.setWindowTitle("Frases prontas")
    w.show()
    sys.exit(app.exec_())