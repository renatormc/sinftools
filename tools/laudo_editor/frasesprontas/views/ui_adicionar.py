# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adicionar.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_adicionar(object):
    def setupUi(self, adicionar):
        adicionar.setObjectName("adicionar")
        adicionar.resize(631, 455)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pluguin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        adicionar.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(adicionar)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.edt_palavras_chave = QtWidgets.QLineEdit(self.centralwidget)
        self.edt_palavras_chave.setObjectName("edt_palavras_chave")
        self.verticalLayout.addWidget(self.edt_palavras_chave)
        self.txt_texto = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_texto.setObjectName("txt_texto")
        self.verticalLayout.addWidget(self.txt_texto)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_ok = QtWidgets.QPushButton(self.centralwidget)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.verticalLayout.addLayout(self.horizontalLayout)
        adicionar.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(adicionar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 21))
        self.menubar.setObjectName("menubar")
        adicionar.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(adicionar)
        self.statusbar.setObjectName("statusbar")
        adicionar.setStatusBar(self.statusbar)

        self.retranslateUi(adicionar)
        QtCore.QMetaObject.connectSlotsByName(adicionar)

    def retranslateUi(self, adicionar):
        _translate = QtCore.QCoreApplication.translate
        adicionar.setWindowTitle(_translate("adicionar", "Adicionar frase ao banco de dados"))
        self.label.setText(_translate("adicionar", "Palavras chave"))
        self.btn_ok.setText(_translate("adicionar", "OK"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    adicionar = QtWidgets.QMainWindow()
    ui = Ui_adicionar()
    ui.setupUi(adicionar)
    adicionar.show()
    sys.exit(app.exec_())

