from ui_{{nome_}} import Ui_{{nome}}
from PyQt5.QtWidgets import QMainWindow

class {{nome}}(QMainWindow):
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
    w = {{nome}}()
    w.show()
    sys.exit(app.exec_())
