from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QTimer
import config as config_
from pathlib import Path
from PyQt5.QtGui import QKeySequence
from sinf.servers.models import *
from sinf.servers.database import db_session
from .helpers import get_disks, get_last_dir, set_last
from .disk_dialog import DiskDialog
from .scripts_maker import get_maker, has_maker
from .ask_wizard_dialog import AskWizardDialog

class ValidationError(Exception):
    pass


class ScriptDialog(QDialog):

    def __init__(self, proc: Process, initial=False):
        super(ScriptDialog, self).__init__()
        self.proc = proc
        self.initial = initial
        self.has_script_maker = has_maker(self.proc)
        self.script = Path(proc.script)
        self.setup_ui()
        text = self.script.read_text(encoding="cp850")
        self.led_dependencies.setText(self.proc.dependencies_ids)
        self.txe_script.setPlainText(text)
        self.ckb_telegram.setChecked(proc.telegram)
        

    def setup_ui(self):
        self.setWindowTitle(f"Editando processo: {self.script}")
        self.setGeometry(500, 50, 900, 400)
        self.setWindowIcon(
            QIcon('{}\\fila\\resources\\icone.png'.format(config_.app_dir)))
        self.main_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        lbl = QLabel(
            "Pressione Ctrl + D para escolher diretório, Ctrl + F para escolher arquivo ou Ctrl + K para escolher disco.")
        lbl.setStyleSheet("color: red;font-size: 10pt;")
        h_layout.addWidget(lbl)
        if self.has_script_maker:
            self.btn_open_script_maker = QPushButton("Assistente")
            self.btn_open_script_maker.setIcon(QIcon(f"{config_.app_dir}\\fila\\resources\\wizard.png"))
            self.btn_open_script_maker.clicked.connect(self.open_script_maker)
            self.btn_open_script_maker.setIconSize(QSize(20,20))
            h_layout.addWidget(self.btn_open_script_maker)
        self.main_layout.addLayout(h_layout)

        self.txe_script = QPlainTextEdit()
        self.txe_script.setStyleSheet(
            "background-color: rgb(64,64,64); color: white; font-size: 10pt;")
        self.main_layout.addWidget(self.txe_script)
        self.main_layout.addWidget(QLabel("Dependências"))

        self.led_dependencies = QLineEdit()
        self.led_dependencies.setPlaceholderText(
            "Entre os ids dos processos dos quais este depende separados por vírgula")
        self.ckb_telegram = QCheckBox("Enviar Telegram")
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.led_dependencies)
        h_layout.addWidget(self.ckb_telegram)

        self.main_layout.addLayout(h_layout)
        self.setLayout(self.main_layout)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok| QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("OK")
        self.button_box.button(QDialogButtonBox.Ok).setIcon(QIcon(f"{config_.app_dir}\\fila\\resources\\ok.png"))
        self.button_box.button(QDialogButtonBox.Ok).setIconSize(QSize(20,20))
        self.button_box.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.button_box.button(QDialogButtonBox.Cancel).setIcon(QIcon(f"{config_.app_dir}\\fila\\resources\\cancel.jpg"))
        self.button_box.button(QDialogButtonBox.Cancel).setIconSize(QSize(20,20))
        self.button_box.accepted.connect(self.accepted)
        self.button_box.rejected.connect(self.rejected)
        self.main_layout.addWidget(self.button_box)
        self.create_shortcuts()

    
    def create_shortcuts(self):
        file_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        file_shortcut.activated.connect(self.choose_file)
        file_shortcut.setEnabled(True)
        dir_shortcut = QShortcut(QKeySequence("Ctrl+D"), self)
        dir_shortcut.activated.connect(self.choose_folder)
        dir_shortcut.setEnabled(True)
        disks_shortcut = QShortcut(QKeySequence("Ctrl+K"), self)
        disks_shortcut.activated.connect(self.choose_disk)
        disks_shortcut.setEnabled(True)

    def showEvent(self, event):
        QDialog.showEvent(self, event)
        QTimer.singleShot(50, self.window_shown)


    def window_shown(self):
        if self.initial and self.has_script_maker:
            dialog = AskWizardDialog()
            dialog.exec_()
            if dialog.ok:
                self.open_script_maker()

    def validate_dependencies(self):
        self.dependencies_ids = []
        try:
            text = self.led_dependencies.displayText().strip()
            if text == "":
                return []
            parts = text.split(",")
            self.dependencies_ids = [int(part.strip()) for part in parts]
        except Exception as e:
            raise ValidationError("As dependências precisam ser declaradas como inteiros separados pro vírgula")

        for id in self.dependencies_ids:
            n = db_session.query(Process).filter_by(id=id).count()
            if id == self.proc.id:
                raise ValidationError(f"O processo não pode depender dele mesmo")
            if n == 0:
                raise ValidationError(f"Não existe um processo de id {id}")

    def validate(self):
        try:
            self.validate_dependencies()
            return True
        except ValidationError as e:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon('{}\\fila\\resources\\icone.png'.format(config_.app_dir)))
            msg.setWindowTitle("Erro")
            msg.setText(str(e))
            msg.exec()
            return False

    # def choose_file(self):
    #     file_name = QFileDialog()
    #     file_name.setFileMode(QFileDialog.ExistingFiles)
    #     file_name.setOption(QFileDialog.DontUseNativeDialog, True)
    #     name, _ = file_name.getOpenFileName(
    #         self, "Escolha um arquivo", get_last_dir())
    #     if name:
    #         path = Path(name)
    #         set_last(path)
    #         self.insert(path)

    def choose_file(self):
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setDirectory(get_last_dir())
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.Detail)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        if dialog.exec_() == QFileDialog.Accepted:
            files = dialog.selectedFiles()
            path = Path(files[0])
            set_last(path)
            self.insert(path)

    def open_script_maker(self):
        dialog = get_maker(self.proc)
        if not dialog:
             QMessageBox.about(self, "Informação", f"Ainda não existe um assistente de criação de script para processos do tipo \"{self.proc.type}\".")
             return
        dialog.exec_()
        if dialog.ok:
            self.txe_script.setPlainText(dialog.script)

    def choose_folder(self):
        name = QFileDialog.getExistingDirectory(
            None, 'Escolha um diretório', get_last_dir())
        if name:
            path = Path(name)
            set_last(path)
            path = str(path)
            if path.endswith("\\"):
                path = path[:-1]
            self.insert(path)

    def insert(self, path):
        text = str(path)
        # if " " in text:
        #     text = f"\"{text}\""
        self.txe_script.insertPlainText(text)

    def get_last_dir(self):
        doc = db_session.query(Document).filter_by(key="last_dir").first()
        return doc.value if doc else "C:\\"

    def set_last(self, path):
        path = Path(path)
        try:
            if path.is_file():
                path = path.parent
            doc = db_session.query(Document).filter_by(key="last_dir").first()
            if not doc:
                doc = Document()
                doc.key = "last_dir"
            doc.value = str(path)
            db_session.add(doc)
            db_session.commit()
        except FileNotFoundError:
            pass

    def choose_disk(self):
        dialog = DiskDialog()
        dialog.exec_()
        if dialog.ok:
            text = dialog.cbx_disk.currentText()
            self.insert(text)


    def accepted(self):
        if self.validate():
            self.script.write_text(self.txe_script.toPlainText(), encoding="cp850")
            db_session.query(Dependecy).filter(Dependecy.blocked_id == self.proc.id).delete()
            for id in self.dependencies_ids:
                dep = Dependecy()
                dep.blocked_id = self.proc.id
                dep.blocker_id = id
                db_session.add(dep)
            self.proc.telegram = self.ckb_telegram.isChecked()
            db_session.commit()
            db_session.add(self.proc)
            db_session.commit()
            self.close()

    def rejected(self):
        self.close()
