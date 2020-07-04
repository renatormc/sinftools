# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ScriptsUFED\Ferramentas\LaudoEditor\inserir_item\widgets\chupa_cabra\view.ui'
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
        self.verticalLayout.addWidget(self.groGeral)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groGeral.setTitle(_translate("Form", "GroupBox"))

import resources_rc
