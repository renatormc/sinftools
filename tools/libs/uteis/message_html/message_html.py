# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog, texto_html):
        Dialog.setObjectName("Dialog")
        Dialog.resize(520, 372)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tdt_informacao = QtWidgets.QTextEdit(Dialog)
        self.tdt_informacao.setReadOnly(True)
        self.tdt_informacao.setObjectName("tdt_informacao")
        self.tdt_informacao.setText(texto_html)
        self.horizontalLayout.addWidget(self.tdt_informacao)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Informação"))

def mostrar_texto(texto):
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog, texto)
    Dialog.show()
    app.exec_()

if __name__ == "__main__":
    mostrar_texto('teste')

