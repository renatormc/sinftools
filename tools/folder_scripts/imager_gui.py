import sys
from PyQt5.Widgets import *

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__()
        self.setupUi()

    def setupUi(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setGeometry(100, 100, 400, 400)
    w.show()
    sys.exit(app.exec_())
    