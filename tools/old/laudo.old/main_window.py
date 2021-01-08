from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from objeto import Objeto
from pathlib import Path
import helpers


class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()

    # def __clear_items(self):
    #     layout = self.ui.scaPics.widget().layout()
    #     for i in reversed(range(layout.count())):
    #         layout.itemAt(i).widget().deleteLater()

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher pasta", ".")
        if folder:
            self.ui.ledPicsFolder.setText(folder)
            path = Path(folder)
            for entry in path.iterdir():
                if helpers.is_image(entry):
                    obj = Objeto(entry)
                    item = QListWidgetItem(self.ui.lsw_pics)
                    item.setSizeHint(obj.sizeHint())
                    self.ui.lsw_pics.addItem(item)
                    self.ui.lsw_pics.setItemWidget(item, obj)

    def connections(self):
        self.ui.btnPicsFolder.clicked.connect(self.choose_folder)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
