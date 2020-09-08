from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from server_thread import ServerThread
import os
import qrcode
from PIL.ImageQt import ImageQt
import json
script_dir = os.path.dirname(os.path.realpath(__file__))


class ReaderServer(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setup_ui()
        self.server_on = False
        # self.setWindowIcon(QtGui.QIcon(
        #     f"{script_dir}\\resources\\icon.png"))
        self.run()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(self)
        central_widget.setLayout(self.main_layout)

        self.lbl_message = QLabel(
            "Abra o aplicativo no Android e aponte a câmera para o código abaixo")
        self.main_layout.addWidget(self.lbl_message)

        self.lbl_qrcode = QLabel()
        self.main_layout.addWidget(self.lbl_qrcode)

        self.generate_qrcode()

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        payload = {
            'url': f""
        }
        qr.add_data('Some data')
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        imageq = ImageQt(img)
        qimage = QtGui.QImage(imageq)
        self.lbl_qrcode.setPixmap(QtGui.QPixmap(qimage))
        # img.save("test.png")

    def closeEvent(self, event):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowIcon(self.windowIcon())
        msg_box.setText("Tem certeza que você deseja fechar?")
        msg_box.setInformativeText(
            'Não feche esta janela enquanto ainda estiver acessando os dados no navegador.')
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

    def run(self):
        self.thread = ServerThread()
        self.thread.start()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = ReaderServer()
    w.show()
    sys.exit(app.exec_())
