from ui_dialog import Ui_Dialog
from PyQt5.QtWidgets import QDialog

class Dialog(QDialog):
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
    w = Dialog()
    w.show()
    sys.exit(app.exec_())