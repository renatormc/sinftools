import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import MainInterface
import os
import codecs
import json
import win32com.client as win32
import re

class Ui_Dialog(object):
    def setupUi(self, Dialog, itens):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 50)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labels = {}
        self.edits ={}
        for i,item in enumerate(itens):
            self.labels["lbl_"+item] = QtWidgets.QLabel(Dialog)
            self.labels["lbl_"+item].setObjectName("lbl_"+item)
            self.labels["lbl_"+item].setText(item)
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, self.labels["lbl_"+item])
            self.edits[item] = QtWidgets.QLineEdit(Dialog)
            self.edits[item].setObjectName(item)
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, self.edits[item])
        
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        QtCore.QMetaObject.connectSlotsByName(Dialog)


class TextDialogWindow(QtWidgets.QDialog):
    ui = None
    finalizou = QtCore.pyqtSignal(object)
    def __init__(self, titulo, itens):
        self.lista_itens = itens
        super(self.__class__, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self, itens)
        #self.setWindowIcon(QtGui.QIcon('C:/ScriptsUFED/Interface/icone.png'))
        self.setWindowTitle(titulo)
        self.ui.buttonBox.accepted.connect(self.ok)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def ok(self):
        resposta = {}
        for item in self.lista_itens:
            resposta[item] = self.ui.edits[item].displayText()
        self.finalizou.emit(resposta)

class input_dialog():
    resultado =None
    def __init__(self,titulo, itens):
        MainW = TextDialogWindow(titulo, itens)
        MainW.finalizou.connect(self.set_resultado)
        MainW.exec_()
        #MainW.show()
 
    def set_resultado(self, res):
            self.resultado = res

class Ui_MainWindow(MainInterface.Ui_MainWindow):
    def __init__(self, main):
        self.main = main
        self.setupUi(main)
        self.connections()
        with codecs.open(os.path.abspath(os.path.dirname(__file__)) + "\\..\\config.json",'r',encoding="utf-8") as arq:
            self.config = json.load(arq)
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        # self.word = win32.Dispatch('Word.Application')
        self.doc = self.word.ActiveDocument
        self.myRange = None
        self.popular_lista()

    def popular_lista(self):
        for entry in os.listdir(self.config['pasta_modelos_inserir']):
            self.lsw_modelos.addItem(entry)

    def connections(self):
        self.btn_ok.clicked.connect(self.ok_click)

    def ok_click(self):
        modelo = self.config['pasta_modelos_inserir'] + '\\' +self.lsw_modelos.currentItem().text()
        current_position = self.word.Selection.Range.Start
        self.word.Selection.InsertFile(modelo)
        self.myRange = self.word.ActiveDocument.Range(Start=current_position,End = self.word.Selection.Range.Start)
        self.substituir_em_range(self.myRange)
        exit()

    def substituir_em_range(self, range):
        comp = re.compile(r'#.*?#')
        lista = []
        for par in range.Paragraphs:
            for item in comp.findall(str(par)):
                if item not in lista and not item.replace(" ", "")[1] == "@":
                    lista.append(item)
        d = input_dialog('Efetuar substituições', lista)
        if d.resultado:
            sub = d.resultado
            for word in sub.keys():
                if sub[word] != '':
                    range.Find.Text = word
                    range.Find.Replacement.Text = sub[word]
                    range.Find.Execute(Replace=2, Forward=True)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
