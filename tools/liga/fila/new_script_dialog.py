from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import config
from database import db_session
from models import *

class NewScriptDialog(QDialog):

    def __init__(self):
        super(NewScriptDialog, self).__init__()
        self.setup_ui()
        self.ok_clicked = False

    def setup_ui(self):
        self.setWindowTitle("Novo processo")
        self.setFixedWidth(300)
        self.setWindowIcon(QIcon('{}\\fila\\resources\\icone.png'.format(config.app_dir)))
        self.main_layout = QVBoxLayout()
        self.led_name = QLineEdit()
        users = db_session.query(User).order_by(User.name).all()
        items = [user.name for user in users]
        self.cbx_perito = QComboBox()
        self.cbx_perito.addItems(items)
        self.cbx_template = QComboBox()
        for key in config.fila_scripts_template.keys():
            self.cbx_template.addItem(key)
        label1 = QLabel("Nome para o script (sem extensão)")
        label2 = QLabel("Perito")
        label3 = QLabel("Tipo")
        self.main_layout.addWidget(label1)
        self.main_layout.addWidget(self.led_name)
        self.main_layout.addWidget(label2)
        self.main_layout.addWidget(self.cbx_perito)
        self.main_layout.addWidget(label3)
        self.main_layout.addWidget(self.cbx_template)
        self.setLayout(self.main_layout)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok| QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("OK")
        self.button_box.button(QDialogButtonBox.Ok).setIcon(QIcon(f"{config.app_dir}\\fila\\resources\\ok.png"))
        self.button_box.button(QDialogButtonBox.Ok).setIconSize(QSize(20,20))
        self.button_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.button_box.button(QDialogButtonBox.Cancel).setIcon(QIcon(f"{config.app_dir}\\fila\\resources\\cancel.jpg"))
        self.button_box.button(QDialogButtonBox.Cancel).setIconSize(QSize(20,20))
        self.button_box.accepted.connect(self.accepted)
        self.button_box.rejected.connect(self.rejected)
        self.main_layout.addWidget(self.button_box)

    def accepted(self):
        perito = self.cbx_perito.currentText()
        if self.led_name.displayText().strip() != "" and perito != "":
            self.ok_clicked = True
            self.close()

    def rejected(self):
        self.ok_clicked = False
        self.close()
