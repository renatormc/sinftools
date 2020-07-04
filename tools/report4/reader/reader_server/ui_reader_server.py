# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\reader_server.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ReaderServer(object):
    def setupUi(self, ReaderServer):
        ReaderServer.setObjectName("ReaderServer")
        ReaderServer.resize(568, 246)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ReaderServer.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ReaderServer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.led_url = QtWidgets.QLineEdit(self.centralwidget)
        self.led_url.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";\n"
"color: rgb(85, 170, 255);")
        self.led_url.setReadOnly(True)
        self.led_url.setObjectName("led_url")
        self.horizontalLayout.addWidget(self.led_url)
        self.btn_copy_url = QtWidgets.QPushButton(self.centralwidget)
        self.btn_copy_url.setObjectName("btn_copy_url")
        self.horizontalLayout.addWidget(self.btn_copy_url)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 3)
        ReaderServer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ReaderServer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 568, 21))
        self.menubar.setObjectName("menubar")
        ReaderServer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ReaderServer)
        self.statusbar.setObjectName("statusbar")
        ReaderServer.setStatusBar(self.statusbar)

        self.retranslateUi(ReaderServer)
        QtCore.QMetaObject.connectSlotsByName(ReaderServer)

    def retranslateUi(self, ReaderServer):
        _translate = QtCore.QCoreApplication.translate
        ReaderServer.setWindowTitle(_translate("ReaderServer", "Analisador de dados"))
        self.textEdit.setHtml(_translate("ReaderServer", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Para vizualizar os dados abra o navegador e navegue até o endereço que aparece abaixo. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Recomenda-se o uso do </span><span style=\" font-size:14pt; color:#aaff7f;\">Mozilla Firefox ou Google Chrome.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ff0000;\">Mantenha esta janela aberta.</span></p></body></html>"))
        self.btn_copy_url.setText(_translate("ReaderServer", "Copiar"))
