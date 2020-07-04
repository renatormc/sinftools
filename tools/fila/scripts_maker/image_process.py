from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from sinf.servers.models import *
from sinf.servers.database import db_session
import config
from helpers import get_last_dir, set_last, get_disks


class ImageProcessDialog(QDialog):

    def __init__(self, process: Process):
        super(ImageProcessDialog, self).__init__()
        self.proc = process
        self.script = ""
        self.ok = False
        self.setup_ui()
        self.load()

    def setup_ui(self):
        self.setWindowTitle(f"Editando processo: {self.proc.script}")
        self.setGeometry(500, 50, 600, 200)
        self.setWindowIcon(
            QIcon('{}\\resources\\icone.png'.format(config.app_dir)))
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.setup_form()
        self.setup_final_buttons()


    def load(self):
        params = self.proc.get_params()
        if params:
            self.led_filename.setText(params['filename'])
            self.led_output_folder.setText(params['output_folder'])
            self.cbx_disk.setCurrentText(params['disk_full'])

    
    def validate(self):
        self.clean_data = {}
        self.clean_data['output_folder'] = self.led_output_folder.displayText().strip()
        if self.clean_data['output_folder'] == "":
            return "Você precisa escolher uma pasta de saída da imagem."
        path = Path(self.clean_data['output_folder'])
        if not path.exists() or not path.is_dir():
            return "A pasta de saída escolhida não é um diretório válido"
        self.clean_data['filename'] = self.led_filename.displayText().strip()
        if self.clean_data['filename'] == "":
            return "Nome do arquivo de saída vazio."
        self.clean_data['disk_full'] = self.cbx_disk.currentText()
        self.clean_data['disk'] = self.clean_data['disk_full'].split()[0].strip()
        self.proc.set_params(self.clean_data)
        db_session.add(self.proc)
        db_session.commit()

    def write_script(self):
        lines = ['@echo off']
        line1 = ['s-check-disk', f"\"{self.clean_data['disk_full']}\"", "&&", "^"]
        image_path = f"{self.clean_data['output_folder']}\\{self.clean_data['filename']}"
        line2 = ['s-ftkimager', self.clean_data['disk'], f"\"{image_path}\"", "--e01", "--verify"]
        lines.append(" ".join(line1))
        lines.append(" ".join(line2))
        self.script = "\n".join(lines)
        

    def setup_form(self):
        layout = QFormLayout()
        self.cbx_disk = QComboBox()
        disks = get_disks()
        for disk in disks:
            self.cbx_disk.addItem(disk)
        layout.addRow(QLabel("Disco"), self.cbx_disk)

        h_layout = QHBoxLayout()
        self.led_output_folder = QLineEdit()
        h_layout.addWidget(self.led_output_folder)
        self.btn_choose_output_folder = QToolButton()
        self.btn_choose_output_folder.setText("...")
        self.btn_choose_output_folder.clicked.connect(self.choose_output_folder)
        h_layout.addWidget(self.btn_choose_output_folder)
        layout.addRow(QLabel("Pasta arquivo de imagem"), h_layout)

        self.led_filename = QLineEdit()
        self.led_filename.setPlaceholderText("Nome do arquivo de imagem sem extensão")
        layout.addRow(QLabel("Nome do arquivo de imagem"), self.led_filename)

        self.main_layout.addLayout(layout)

    def setup_final_buttons(self):
        layout = QHBoxLayout()

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setIcon(QIcon(f"{config.app_dir}\\resources\\ok.png"))
        self.btn_ok.setIconSize(QSize(20, 20))
        self.btn_ok.clicked.connect(self.ok_click)
        layout.addWidget(self.btn_ok)
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_cancel.setIcon(
            QIcon(f"{config.app_dir}\\resources\\cancel.jpg"))
        self.btn_cancel.setIconSize(QSize(20, 20))
        layout.addWidget(self.btn_cancel)
        self.main_layout.addLayout(layout)

    def choose_output_folder(self):
        name = QFileDialog.getExistingDirectory(
            None, 'Escolha um diretório', get_last_dir())
        if name:
            path = Path(name)
            self.led_output_folder.setText(str(path.absolute()))
            set_last(path)


    def ok_click(self):
        err = self.validate()
        if err:
            QMessageBox.warning(self, "Erro", err)
            return
        self.write_script()
        self.ok = True
        self.close()

    def cancel(self):
        self.ok = False
        self.close()
