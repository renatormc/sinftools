from ui_widget import Ui_Widget
from PyQt5.QtWidgets import QWidget

class Widget(QWidget):
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
    w = Widget()
    w.show()
    sys.exit(app.exec_())