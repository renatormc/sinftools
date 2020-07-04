from reader_server.ui_reader_server import Ui_ReaderServer
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtGui
from reader_server.server_thread import ServerThread
import socket
import clipboard
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

def get_available_port():
    port = 5000
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            port += 1
            continue
        return port

class ReaderServer(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_ReaderServer()
        self.ui.setupUi(self)
        self.connections()
        self.server_on = False
        self.setWindowIcon(QtGui.QIcon(
            f"{script_dir}\\resources\\icon.png"))
    
        
    def connections(self):
        self.ui.btn_copy_url.clicked.connect(self.copy_url)

    def closeEvent (self, event):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setText("Tem certeza que você deseja fechar?")
        msg_box.setInformativeText('Não feche esta janela enquanto ainda estiver acessando os dados no navegador.')
        msg_box.setWindowTitle('Atenção!')
        btn_yes = msg_box.addButton(QMessageBox.Yes)
        btn_no = msg_box.addButton(QMessageBox.No)
        msg_box.setDefaultButton(btn_no)
        btn_yes.setText("Sim")
        btn_no.setText("Não")
        msg_box.exec_()
        if msg_box.clickedButton() == btn_yes:
            event.accept()
        else:
            event.ignore()

    def copy_url(self):
        clipboard.copy(self.ui.led_url.displayText())

    def run(self):
        self.thread = ServerThread()
        self.thread.port = get_available_port()
        self.ui.led_url.setText(f"http://localhost:{self.thread.port}")
        self.thread.start()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ReaderServer()
    w.show()
    sys.exit(app.exec_())
