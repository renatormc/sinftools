from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import QDialog, QMessageBox
import win32com.client
import config
import json
from doc_printer import DocPrinter
import helpers as hp
from PyQt5.QtGui import QIcon
import os


class MainWindow(QDialog):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_ui()
        self.connections()
        self.populatePrinters()
        self.load_config()

    def setup_ui(self):
        icon = QIcon(str(config.app_dir / "resources/print-icon.png"))
        self.setWindowIcon(icon)
        self.ui.btnConfigPrinters.setIcon(icon)

    def connections(self):
        self.ui.btnPrint.clicked.connect(self.print_files)
        self.ui.btnConfigPrinters.clicked.connect(self.open_printers_config)

    def open_printers_config(self):
        os.system("control printers")
        self.close()

    def populatePrinters(self):
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(".", "root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_Printer")
        for objItem in colItems:
            self.ui.cbxPrinter.addItem(objItem.Name)
            self.ui.cbxPrinterDuplex.addItem(objItem.Name)



    def print_files(self):
        try:
            self.save_config()
            docs = hp.find_docs()
            with DocPrinter(self.get_printers()) as dp:
                if docs['capa']:
                    dp.print_doc(docs['capa'], self.ui.spbCover.value(), self.ui.chkCapa.isChecked())
                if docs['laudo']:
                    dp.print_doc(docs['laudo'], self.ui.spbLaudo.value(), self.ui.chkLaudo.isChecked(), save_pdf=self.ui.chkSavePdf.isChecked())
                if docs['midia']:
                    dp.print_doc(docs['midia'], self.ui.spbMidia.value(), self.ui.chkMidia.isChecked())
            QMessageBox.information(self, 'Impressão iniciada', "Impressão enviada para a impressora", QMessageBox.Ok)
            self.close()        
        except Exception as e:
            QMessageBox.warning(self, 'Houve um erro', str(e), QMessageBox.Ok)

    def get_printers(self):
        return {
            'simple': self.ui.cbxPrinter.currentText(),
            'duplex': self.ui.cbxPrinterDuplex.currentText()
        }

    def save_config(self):
        data = {
            'simple': self.ui.cbxPrinter.currentText(),
            'duplex': self.ui.cbxPrinterDuplex.currentText()
        }
        config.config_file.write_text(json.dumps(
            data, ensure_ascii=False, indent=4), encoding="utf-8")

    def load_config(self):
        try:
            with config.config_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.ui.cbxPrinter.setCurrentText(data['simple'])
            self.ui.cbxPrinterDuplex.setCurrentText(data['duplex'])
        except:
            pass


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
