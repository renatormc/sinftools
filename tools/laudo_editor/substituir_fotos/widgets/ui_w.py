# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'w.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_W(object):
    def setupUi(self, W):
        W.setObjectName("W")
        W.resize(537, 46)
        self.formLayout = QtWidgets.QFormLayout(W)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTag = QtWidgets.QLabel(W)
        self.lblTag.setObjectName("lblTag")
        self.horizontalLayout.addWidget(self.lblTag)
        self.edtArquivo = QtWidgets.QLineEdit(W)
        self.edtArquivo.setObjectName("edtArquivo")
        self.horizontalLayout.addWidget(self.edtArquivo)
        self.btnEscolher = QtWidgets.QToolButton(W)
        self.btnEscolher.setObjectName("btnEscolher")
        self.horizontalLayout.addWidget(self.btnEscolher)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)

        self.retranslateUi(W)
        QtCore.QMetaObject.connectSlotsByName(W)

    def retranslateUi(self, W):
        _translate = QtCore.QCoreApplication.translate
        W.setWindowTitle(_translate("W", "W"))
        self.lblTag.setText(_translate("W", "TAG"))
        self.btnEscolher.setText(_translate("W", "..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    W = QtWidgets.QWidget()
    ui = Ui_W()
    ui.setupUi(W)
    W.show()
    sys.exit(app.exec_())

