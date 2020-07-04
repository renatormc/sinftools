from ui_android_macro import Ui_AndroidMacro
from PyQt5.QtWidgets import QMainWindow

class AndroidMacro2(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_AndroidMacro()
        self.ui.setupUi(self)
        self.connections()

    def connections(self):
        pass

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = AndroidMacro2()
    w.show()
    sys.exit(app.exec_())
