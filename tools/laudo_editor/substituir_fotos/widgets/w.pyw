from widgets.ui_w import Ui_W
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSignal
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

class W(QWidget):
    mudou_diretorio = pyqtSignal(str)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_W()
        self.ui.setupUi(self)
        self.connections()
        self.dir = "C:\\"
        

    def connections(self):
        self.ui.btnEscolher.clicked.connect(self.escolher)

    def setDir(self, directory):
        self.dir = directory

    def escolher(self):
        nome = QFileDialog.getOpenFileName(self, 'Open file', self.dir,"Image files (*.jpg *.gif *.png)")
        dire = os.path.dirname(nome[0])
        if dire != self.dir:
            self.mudou_diretorio.emit(dire)
        self.ui.edtArquivo.setText(nome[0])

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = W()
    w.show()
    sys.exit(app.exec_())
