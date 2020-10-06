from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from pathlib import Path
import helpers as hp

class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.folder = Path(".").absolute()
        self.load_pericias()

    @property
    def folder(self):
        return Path(self.ui.led_folder.displayText())

    @folder.setter
    def folder(self, value):
        folder = Path(value)
        self.ui.led_folder.setText(str(folder))

    @property
    def pericia(self):
        item = self.ui.cbx_pericia.currentText()
        return item.split("-")[0].strip()

    def connections(self):
        self.ui.btn_choose_folder.clicked.connect(self.choose_folder)
        self.ui.btn_ok.clicked.connect(self.upload)

    def load_pericias(self):
        pericias = hp.get_pericias()
        self.ui.cbx_pericia.clear()
        self.ui.cbx_pericia.addItems(pericias)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, 'Selecione um diretório', str(self.folder))
        if folder:
            self.folder = folder

    def upload(self):
        ok = hp.upload_fotos(self.folder, self.pericia)
        text = "Upload realizado" if ok else "Houve um erro"
        msg = QMessageBox()
        msg.setWindowTitle("Tudo certo")
        msg.setText(text)
        msg.exec()
        self.close()
        


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())