from ui_main_window import Ui_MAinWindow
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_{{nome}}()
        self.ui.setupUi(self)
        self.connections()

    def connections(self):
        pass

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())