# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'marker_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511, 287)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txe_marker = QtWidgets.QPlainTextEdit(Dialog)
        self.txe_marker.setReadOnly(True)
        self.txe_marker.setObjectName("txe_marker")
        self.verticalLayout.addWidget(self.txe_marker)
        self.bbx_box = QtWidgets.QDialogButtonBox(Dialog)
        self.bbx_box.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_box.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.bbx_box.setObjectName("bbx_box")
        self.verticalLayout.addWidget(self.bbx_box)

        self.retranslateUi(Dialog)
        self.bbx_box.accepted.connect(Dialog.accept)
        self.bbx_box.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Marker"))
