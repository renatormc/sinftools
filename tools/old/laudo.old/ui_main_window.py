# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(888, 589)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ledPicsFolder = QtWidgets.QLineEdit(self.centralwidget)
        self.ledPicsFolder.setReadOnly(True)
        self.ledPicsFolder.setObjectName("ledPicsFolder")
        self.horizontalLayout.addWidget(self.ledPicsFolder)
        self.btnPicsFolder = QtWidgets.QToolButton(self.centralwidget)
        self.btnPicsFolder.setObjectName("btnPicsFolder")
        self.horizontalLayout.addWidget(self.btnPicsFolder)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layPics = QtWidgets.QVBoxLayout()
        self.layPics.setObjectName("layPics")
        self.verticalLayout.addLayout(self.layPics)
        self.lsw_pics = QtWidgets.QListWidget(self.centralwidget)
        self.lsw_pics.setDragEnabled(True)
        self.lsw_pics.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.lsw_pics.setAlternatingRowColors(True)
        self.lsw_pics.setObjectName("lsw_pics")
        self.verticalLayout.addWidget(self.lsw_pics)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 888, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Coloque todas as fotos dos objetos em um pasta e em seguida a selecione</span></p></body></html>"))
        self.btnPicsFolder.setText(_translate("MainWindow", "..."))
