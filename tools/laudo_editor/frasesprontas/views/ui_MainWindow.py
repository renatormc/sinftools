# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 461)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/pluguin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edtPesquisar = QtWidgets.QLineEdit(self.centralwidget)
        self.edtPesquisar.setObjectName("edtPesquisar")
        self.horizontalLayout.addWidget(self.edtPesquisar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.cbxCampo = QtWidgets.QComboBox(self.centralwidget)
        self.cbxCampo.setMinimumSize(QtCore.QSize(172, 0))
        self.cbxCampo.setObjectName("cbxCampo")
        self.cbxCampo.addItem("")
        self.cbxCampo.addItem("")
        self.horizontalLayout_2.addWidget(self.cbxCampo)
        self.btnDeletar = QtWidgets.QPushButton(self.centralwidget)
        self.btnDeletar.setObjectName("btnDeletar")
        self.horizontalLayout_2.addWidget(self.btnDeletar)
        self.btnPesquisar = QtWidgets.QPushButton(self.centralwidget)
        self.btnPesquisar.setObjectName("btnPesquisar")
        self.horizontalLayout_2.addWidget(self.btnPesquisar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lswResultados = QtWidgets.QListWidget(self.centralwidget)
        self.lswResultados.setStyleSheet("alternate-background-color: #b5e7a0;background-color: white;")
        self.lswResultados.setAlternatingRowColors(True)
        self.lswResultados.setTextElideMode(QtCore.Qt.ElideNone)
        self.lswResultados.setWordWrap(True)
        self.lswResultados.setObjectName("lswResultados")
        self.verticalLayout.addWidget(self.lswResultados)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pesquisar frase"))
        self.cbxCampo.setItemText(0, _translate("MainWindow", "Conteúdo"))
        self.cbxCampo.setItemText(1, _translate("MainWindow", "Palavras-chave"))
        self.btnDeletar.setText(_translate("MainWindow", "Deletar"))
        self.btnPesquisar.setText(_translate("MainWindow", "Pesquisar"))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

