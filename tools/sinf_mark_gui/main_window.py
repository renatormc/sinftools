from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from pathlib import Path
from scanner import Scanner

class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.ui.led_folder.setText(str(Path(".").absolute()))
        

    def connections(self):
        self.ui.btn_choose_folder.clicked.connect(self.choose_dir)
        self.ui.btn_scan_drives.clicked.connect(self.scan_drives)

    @property
    def folder(self):
        return Path(self.ui.led_folder.displayText())


    def choose_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Escolher diretório", str(self.folder))
        if directory:
            self.ui.led_folder.setText(str(Path(directory).absolute()))
    
    def print_status_bar(self, message):
        self.statusBar().showMessage(message)


    def scan_drives(self):
        self.scanner = Scanner()
        def onfinish():
            print(self.scanner.folders)
        self.scanner.finish
        self.scanner.print_message.connect(self.statusBar().showMessage)
        self.scanner.start()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())