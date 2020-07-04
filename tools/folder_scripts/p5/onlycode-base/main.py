from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUI()
        self.connections()
      

    def setupUI(self):
        self.setWindowIcon(QIcon('{}\\resources\\icone.png'.format(script_dir)))
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

    def connections(self):
        pass
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setGeometry(500,300,800,600)
    w.setWindowTitle("Window")
    w.show()
    sys.exit(app.exec_())