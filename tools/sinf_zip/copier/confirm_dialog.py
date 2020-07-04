from PyQt5.QtWidgets import QDialog, QVBoxLayout,  QApplication, QLabel, QSizePolicy, QPushButton, QSpacerItem, QHBoxLayout
from PyQt5.QtGui import QIcon
import sys
import os


script_dir = os.path.dirname(os.path.realpath(__file__))

class ConfirmDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUI()
        self.connections()
        self.set_message("Insira o CD de número 3")
        self.ok_clicked = False
                        
             
    def setupUI(self):
        self.setGeometry(500,300,300,150)
        self.setWindowTitle("Insira nova mídia")
        self.setWindowIcon(QIcon('{}\\resources\\icone.png'.format(script_dir)))
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.lbl_message = QLabel()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancelar")

        lay_horizontal = QHBoxLayout()
        lay_horizontal.addSpacerItem(spacer)
        lay_horizontal.addWidget(self.btn_ok)
        lay_horizontal.addWidget(self.btn_cancel)

        self.main_layout.addWidget(self.lbl_message)
        self.main_layout.addLayout(lay_horizontal)

    def set_message(self, message):
        self.lbl_message.setText(message)
        self.lbl_message.setStyleSheet("font-size: 13pt; color: red; font-weight: bold;")

    def closeEvent(self, a0):
        self.ok_clicked = False
        return super().closeEvent(a0)

    def cancel(self):
        self.ok_clicked = False
        self.close()

    def ok(self):
        self.ok_clicked = True
        self.close()


    def connections(self):
        pass
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())