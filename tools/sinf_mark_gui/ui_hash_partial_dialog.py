# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hash_partial_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HashPartialDialog(object):
    def setupUi(self, HashPartialDialog):
        HashPartialDialog.setObjectName("HashPartialDialog")
        HashPartialDialog.resize(283, 77)
        self.verticalLayout = QtWidgets.QVBoxLayout(HashPartialDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.typeLabel = QtWidgets.QLabel(HashPartialDialog)
        self.typeLabel.setObjectName("typeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.typeLabel)
        self.cbx_subtype = QtWidgets.QComboBox(HashPartialDialog)
        self.cbx_subtype.setObjectName("cbx_subtype")
        self.cbx_subtype.addItem("")
        self.cbx_subtype.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbx_subtype)
        self.verticalLayout.addLayout(self.formLayout)
        self.bbx_box = QtWidgets.QDialogButtonBox(HashPartialDialog)
        self.bbx_box.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bbx_box.setCenterButtons(False)
        self.bbx_box.setObjectName("bbx_box")
        self.verticalLayout.addWidget(self.bbx_box)

        self.retranslateUi(HashPartialDialog)
        QtCore.QMetaObject.connectSlotsByName(HashPartialDialog)

    def retranslateUi(self, HashPartialDialog):
        _translate = QtCore.QCoreApplication.translate
        HashPartialDialog.setWindowTitle(_translate("HashPartialDialog", "Hash Partial Dialog"))
        self.typeLabel.setText(_translate("HashPartialDialog", "Subtype"))
        self.cbx_subtype.setItemText(0, _translate("HashPartialDialog", "iped_images"))
        self.cbx_subtype.setItemText(1, _translate("HashPartialDialog", "iped_results"))
