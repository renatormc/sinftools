# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

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
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainW = TextDialogWindow(titulo, itens)
        MainW.finalizou.connect(self.set_resultado)
        MainW.show()
        app.exec_()
 
    def set_resultado(self, res):
            self.resultado = res
            
if __name__ == "__main__":
    d = input_dialog('Valores',['Nome','Altura','Endereço','teste1','teste2'])
    if d.resultado:
        print(d.resultado)
    
