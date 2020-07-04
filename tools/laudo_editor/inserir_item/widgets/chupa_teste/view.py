# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ScriptsUFED\Ferramentas\LaudoEditor\inserir_item\widgets\chupa_teste\view.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(556, 179)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groGeral = QtWidgets.QGroupBox(Form)
        self.groGeral.setObjectName("groGeral")
        self.toolButton = QtWidgets.QToolButton(self.groGeral)
        self.toolButton.setGeometry(QtCore.QRect(180, 80, 25, 19))
        self.toolButton.setObjectName("toolButton")
        self.pushButton = QtWidgets.QPushButton(self.groGeral)
        self.pushButton.setGeometry(QtCore.QRect(120, 50, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.checkBox = QtWidgets.QCheckBox(self.groGeral)
        self.checkBox.setGeometry(QtCore.QRect(340, 70, 70, 17))
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.groGeral)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groGeral.setTitle(_translate("Form", "GroupBox"))
        self.toolButton.setText(_translate("Form", "..."))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.checkBox.setText(_translate("Form", "CheckBox"))

import resources_rc
