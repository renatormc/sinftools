# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\ScriptsUFED\Ferramentas\LaudoEditor\inserir_item\widgets\celular\view.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(636, 316)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(636, 316))
        Form.setStyleSheet("#groGeral {font-weight: 900; color:red}\n"
"#Form{background-color:white}\n"
"")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groGeral = QtWidgets.QGroupBox(Form)
        self.groGeral.setStyleSheet("")
        self.groGeral.setObjectName("groGeral")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groGeral)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groGeral)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.sequNciaChip1Label = QtWidgets.QLabel(self.groupBox_2)
        self.sequNciaChip1Label.setObjectName("sequNciaChip1Label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sequNciaChip1Label)
        self.sequenciaChip1LineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.sequenciaChip1LineEdit.setObjectName("sequenciaChip1LineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sequenciaChip1LineEdit)
        self.seq2_label = QtWidgets.QLabel(self.groupBox_2)
        self.seq2_label.setObjectName("seq2_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.seq2_label)
        self.sequenciaChip2LineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.sequenciaChip2LineEdit.setObjectName("sequenciaChip2LineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sequenciaChip2LineEdit)
        self.operadoraChip1Label = QtWidgets.QLabel(self.groupBox_2)
        self.operadoraChip1Label.setObjectName("operadoraChip1Label")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.operadoraChip1Label)
        self.operadoraChip1LineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.operadoraChip1LineEdit.setObjectName("operadoraChip1LineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.operadoraChip1LineEdit)
        self.operadoraChip2Label = QtWidgets.QLabel(self.groupBox_2)
        self.operadoraChip2Label.setObjectName("operadoraChip2Label")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.operadoraChip2Label)
        self.operadoraChip2LineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.operadoraChip2LineEdit.setObjectName("operadoraChip2LineEdit")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.operadoraChip2LineEdit)
        self.marcaSDLabel = QtWidgets.QLabel(self.groupBox_2)
        self.marcaSDLabel.setObjectName("marcaSDLabel")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.marcaSDLabel)
        self.marcaSDLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.marcaSDLineEdit.setObjectName("marcaSDLineEdit")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.marcaSDLineEdit)
        self.capacidadeSDLabel = QtWidgets.QLabel(self.groupBox_2)
        self.capacidadeSDLabel.setObjectName("capacidadeSDLabel")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.capacidadeSDLabel)
        self.capacidadeSDLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.capacidadeSDLineEdit.setObjectName("capacidadeSDLineEdit")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.capacidadeSDLineEdit)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.groGeral)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.marcaLabel = QtWidgets.QLabel(self.groupBox)
        self.marcaLabel.setObjectName("marcaLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.marcaLabel)
        self.marcaLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.marcaLineEdit.setObjectName("marcaLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.marcaLineEdit)
        self.modeloLabel = QtWidgets.QLabel(self.groupBox)
        self.modeloLabel.setObjectName("modeloLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.modeloLabel)
        self.modeloLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.modeloLineEdit.setObjectName("modeloLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.modeloLineEdit)
        self.imeiLabel = QtWidgets.QLabel(self.groupBox)
        self.imeiLabel.setObjectName("imeiLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.imeiLabel)
        self.imeiLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.imeiLineEdit.setObjectName("imeiLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.imeiLineEdit)
        self.marcaDaBateriaLabel = QtWidgets.QLabel(self.groupBox)
        self.marcaDaBateriaLabel.setObjectName("marcaDaBateriaLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.marcaDaBateriaLabel)
        self.marcaBateriaLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.marcaBateriaLineEdit.setObjectName("marcaBateriaLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.marcaBateriaLineEdit)
        self.nomeObjetoLabel = QtWidgets.QLabel(self.groupBox)
        self.nomeObjetoLabel.setObjectName("nomeObjetoLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.nomeObjetoLabel)
        self.nomeObjetoLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nomeObjetoLineEdit.setObjectName("nomeObjetoLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.nomeObjetoLineEdit)
        self.legendaDosDispositivosLabel = QtWidgets.QLabel(self.groupBox)
        self.legendaDosDispositivosLabel.setObjectName("legendaDosDispositivosLabel")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.legendaDosDispositivosLabel)
        self.legendaDispositivosLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.legendaDispositivosLineEdit.setObjectName("legendaDispositivosLineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.legendaDispositivosLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout.addWidget(self.groupBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEditFotoCelular = QtWidgets.QLineEdit(self.groGeral)
        self.lineEditFotoCelular.setObjectName("lineEditFotoCelular")
        self.gridLayout_2.addWidget(self.lineEditFotoCelular, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groGeral)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.btnFotoCelular = QtWidgets.QToolButton(self.groGeral)
        self.btnFotoCelular.setObjectName("btnFotoCelular")
        self.gridLayout_2.addWidget(self.btnFotoCelular, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groGeral)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.btnFotoEtiqueta = QtWidgets.QToolButton(self.groGeral)
        self.btnFotoEtiqueta.setObjectName("btnFotoEtiqueta")
        self.gridLayout_2.addWidget(self.btnFotoEtiqueta, 1, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.groGeral)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditFotoEtiqueta = QtWidgets.QLineEdit(self.groGeral)
        self.lineEditFotoEtiqueta.setObjectName("lineEditFotoEtiqueta")
        self.gridLayout_2.addWidget(self.lineEditFotoEtiqueta, 1, 2, 1, 1)
        self.lineEditFotoDispositivos = QtWidgets.QLineEdit(self.groGeral)
        self.lineEditFotoDispositivos.setObjectName("lineEditFotoDispositivos")
        self.gridLayout_2.addWidget(self.lineEditFotoDispositivos, 2, 2, 1, 1)
        self.btnFotoDispositivos = QtWidgets.QToolButton(self.groGeral)
        self.btnFotoDispositivos.setObjectName("btnFotoDispositivos")
        self.gridLayout_2.addWidget(self.btnFotoDispositivos, 2, 3, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)
        self.verticalLayout_3.addWidget(self.groGeral)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groGeral.setTitle(_translate("Form", "Celular"))
        self.groupBox_2.setTitle(_translate("Form", "Disipositivos"))
        self.sequNciaChip1Label.setText(_translate("Form", "Sequência chip1"))
        self.seq2_label.setText(_translate("Form", "Sequência Chip2"))
        self.operadoraChip1Label.setText(_translate("Form", "Operadora Chip 1"))
        self.operadoraChip2Label.setText(_translate("Form", "Operadora Chip2"))
        self.marcaSDLabel.setText(_translate("Form", "Marca SD"))
        self.capacidadeSDLabel.setText(_translate("Form", "Capacidade SD"))
        self.groupBox.setTitle(_translate("Form", "Informações básicas"))
        self.marcaLabel.setText(_translate("Form", "Marca"))
        self.modeloLabel.setText(_translate("Form", "Modelo"))
        self.imeiLabel.setText(_translate("Form", "IMEI"))
        self.marcaDaBateriaLabel.setText(_translate("Form", "Marca da bateria"))
        self.nomeObjetoLabel.setText(_translate("Form", "Nome do objeto"))
        self.legendaDosDispositivosLabel.setText(_translate("Form", "Legenda dos dispositivos"))
        self.label_3.setText(_translate("Form", "Foto Dispositivos"))
        self.btnFotoCelular.setText(_translate("Form", "..."))
        self.label_2.setText(_translate("Form", "Foto Etiqueta"))
        self.btnFotoEtiqueta.setText(_translate("Form", "..."))
        self.label.setText(_translate("Form", "Foto Celular"))
        self.btnFotoDispositivos.setText(_translate("Form", "..."))

import resources_rc