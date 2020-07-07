from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import config

class AskWizardDialog(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.ok = False
        self.setup_ui()

    def setup_ui(self):
        self.setWindowIcon(QIcon(f"{config.app_dir}\\fila\\resources\\icone.png"))
        self.setWindowTitle("Experimento o assistente")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        label = QLabel("Você tem a opção de editar o script manualmente ou utilizar o assistente. \nO que gostaria de fazer?")
        label.setStyleSheet("font-size: 12pt;")
        self.main_layout.addWidget(label)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("Utilizar assistente")
        self.button_box.button(QDialogButtonBox.Ok).setIcon(QIcon(f"{config.app_dir}\\fila\\resources\\wizard.png"))
        self.button_box.button(QDialogButtonBox.Ok).setIconSize(QSize(20,20))
        self.button_box.button(QDialogButtonBox.Cancel).setText("Editar script manualmente")
        self.button_box.button(QDialogButtonBox.Cancel).setIcon(QIcon(f"{config.app_dir}\\fila\\resources\\script.png"))
        self.button_box.button(QDialogButtonBox.Cancel).setIconSize(QSize(20,20))
        self.button_box.accepted.connect(self.accepted)
        self.button_box.rejected.connect(self.rejected)
        self.main_layout.addWidget(self.button_box)

    def accepted(self):
        self.ok = True
        self.close()

    def rejected(self):
        self.ok = False
        self.close()
