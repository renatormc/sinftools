from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from models import *
from database import db_session
import config
from ..helpers import get_last_dir, set_last


class IpedProcessDialog(QDialog):

    def __init__(self, process: Process):
        super(IpedProcessDialog, self).__init__()
        self.proc = process
        self.script = ""
        self.ok = False
        self.setup_ui()
        self.load()

    def setup_ui(self):
        self.setWindowTitle(f"Editando processo: {self.proc.script}")
        self.setGeometry(500, 50, 600, 300)
        self.setWindowIcon(
            QIcon('{}\\fila\\resources\\icone.png'.format(config.app_dir)))
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.setup_form()
        self.setup_final_buttons()

    def load(self):
        params = self.proc.get_params()
        if params:
            self.led_output_folder.setText(params['output_folder'])
            self.cbx_profile.setCurrentText(params['profile'])
            self.txe_sources.setPlainText("\n".join(params['sources']))
            self.ckb_portable.setChecked(params['portable'])

    def validate(self):
        self.clean_data = {}
        self.clean_data['output_folder'] = self.led_output_folder.displayText(
        ).strip()
        if self.clean_data['output_folder'] == "":
            return "Você precisa escolher uma pasta de saída."
        path = Path(self.clean_data['output_folder'])
        if not path.exists() or not path.is_dir():
            return "A pasta de saída escolhida não é um diretório válido"
        sources = self.txe_sources.toPlainText().strip()
        if sources == "":
            return "Você não definiu as fontes de dados."
        self.clean_data['sources'] = sources.split("\n")
        for item in self.clean_data['sources']:
            path = Path(item)
            if not path.exists():
                return f"Arquivo ou pasta inexistente: \"{path}\""
        self.clean_data['profile'] = self.cbx_profile.currentText()
        self.clean_data['portable'] = self.ckb_portable.isChecked()
        self.proc.set_params(self.clean_data)
        db_session.add(self.proc)
        db_session.commit()

    def write_script(self):
        iped_command = 's-iped' if config.iped_defaul else 'iped'
        args = [iped_command, '-profile', self.clean_data['profile'], '--nogui']
        if self.clean_data['portable']:
            args.append('--portable')
        for entry in self.clean_data['sources']:
            args += ['-d', f"\"{entry}\""]
        args += ['-o', f"\"{self.clean_data['output_folder']}\""]
        lines = ["@echo off", " ".join(args)]
        self.script = "\n".join(lines)
        

    def setup_form(self):
        layout = QFormLayout()
        self.cbx_profile = QComboBox()
        profiles_folder = config.iped_folder / "profiles/pt-BR"
        for entry in profiles_folder.iterdir():
            if entry.is_dir():
                self.cbx_profile.addItem(entry.name)
        layout.addRow(QLabel("Perfil"), self.cbx_profile)

        h_layout = QHBoxLayout()
        self.led_output_folder = QLineEdit()
        h_layout.addWidget(self.led_output_folder)
        self.btn_choose_output_folder = QToolButton()
        self.btn_choose_output_folder.setText("...")
        self.btn_choose_output_folder.clicked.connect(self.choose_output_folder)
        h_layout.addWidget(self.btn_choose_output_folder)
        layout.addRow(QLabel("Pasta de saída"), h_layout)

        h_layout = QHBoxLayout()
        self.txe_sources = QPlainTextEdit()
        self.txe_sources.setPlaceholderText("Uma fonte por linha")
        h_layout.addWidget(self.txe_sources)
        self.btn_choose_sources = QToolButton()
        self.btn_choose_sources.setText("...")
        self.btn_choose_sources.clicked.connect(self.choose_sources)
        h_layout.addWidget(self.btn_choose_sources)
        layout.addRow(QLabel("Fontes"), h_layout)

        self.ckb_portable = QCheckBox("Portable")
        self.ckb_portable.setChecked(False)
        layout.addRow(QLabel(), self.ckb_portable)

        self.main_layout.addLayout(layout)

    def setup_final_buttons(self):
        layout = QHBoxLayout()

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setIcon(QIcon(f"{config.app_dir}\\fila\\resources\\ok.png"))
        self.btn_ok.setIconSize(QSize(20, 20))
        self.btn_ok.clicked.connect(self.ok_click)
        layout.addWidget(self.btn_ok)
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_cancel.setIcon(
            QIcon(f"{config.app_dir}\\fila\\resources\\cancel.jpg"))
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

    def choose_sources(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(get_last_dir())
        dialog.setFileMode(QFileDialog.ExistingFiles)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        if dialog.exec_() == QFileDialog.Accepted:
            files = dialog.selectedFiles()
            lines = [line.strip() for line in self.txe_sources.toPlainText().strip().split("\n") if line.strip() != ""]
            for f in files:
                lines.append(f.replace("/", "\\"))
            self.txe_sources.setPlainText("\n".join(lines))
            set_last(files[0])

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
