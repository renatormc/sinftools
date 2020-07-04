from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QDialog, QApplication, QLabel, QSizePolicy, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import sys
import os
import codecs
import json
from worker import Worker
import tempfile
from PyQt5.QtCore import Qt
import shutil
import settings
from subprocess import Popen

script_dir = os.path.dirname(os.path.realpath(__file__))

class Window(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.message = ""
        self.setupUI()
        self.connections()
        self.drive = sys.argv[1]
        self.read_config()
        self.tempdir = os.path.join(tempfile.gettempdir(), "sinf_temp")
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
        os.makedirs(self.tempdir)
        self.timer = QTimer()
        self.timer.timeout.connect(self.blink_label)
        self.timer.start(200)
        self.message_visible = False
                
    def read_config(self):         
        with codecs.open(os.path.join(self.drive, ".sinf", "config.json"), "r", "utf-8") as f:
            self.config = json.load(f)
       
        
    def blink_label(self):
        self.message_visible = not self.message_visible
        text = self.message if self.message_visible else ""
        self.lbl_message.setText(text)

    def hide_message(self):
        self.lbl_message.setVisible(False)

    def set_message(self, message):
        self.message = message

    def setupUI(self):
        self.setWindowIcon(QIcon('{}\\icon.png'.format(settings.app_dir)))
        self.setWindowTitle("Extair arquivos")
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)


        self.lbl_message = QLabel(self.message)
        self.lbl_message.setStyleSheet("font-size: 15pt; color: red;")
        self.lbl_message.setAlignment(Qt.AlignCenter)
        self.general_pg_bar = QProgressBar()
        self.general_pg_bar.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        label1 = QLabel("Progresso geral")
        label2=  QLabel("Progresso mídia corrente")
        self.btn_extract = QPushButton("Escolher pasta para extração")
        self.btn_extract.setStyleSheet("background-color: green; color: white; font-size: 15pt;")
        self.btn_extract.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.individual_pg_bar = QProgressBar()
        self.individual_pg_bar.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        lay_progress = QVBoxLayout()
        self.wid_progress = QWidget()
        self.wid_progress.setVisible(False)
        self.wid_progress.setLayout(lay_progress)
        lay_progress.addWidget(label1)
        lay_progress.addWidget(self.general_pg_bar)
        lay_progress.addWidget(label2)
        lay_progress.addWidget(self.individual_pg_bar)
        
        
        self.main_layout.addWidget(self.lbl_message)
        self.main_layout.addWidget(self.btn_extract)
        self.main_layout.addWidget(self.wid_progress)

      
    def update_progress(self, general, individual):
        self.general_pg_bar.setValue(general)
        self.individual_pg_bar.setValue(individual)

    def extract(self):
        first_dir = os.getenv("USERPROFILE")
        self.extract_dir = QFileDialog.getExistingDirectory(self, 'Selecione um diretório', first_dir)
        if self.extract_dir:
            self.worker = Worker(self)
            self.worker.update_progress.connect(self.update_progress)
            self.worker.show_message.connect(self.set_message)
            self.worker.finished.connect(self.finished)
            self.worker.start()
            self.wid_progress.setVisible(True)
            self.btn_extract.setVisible(False)

    def get_current_midia(self):
        file = f"{self.drive}\\.sinf\\current_midia.txt"
        if os.path.exists(file):
            with open(file, "r") as f:
                value = int(f.read())
            return value

    def finished(self):
        exec = os.path.join(self.tempdir, "dados.exe")
        cmd = f"{exec} -o\"{self.extract_dir}\" -y"
        os.system(cmd)
        os.system(f"explorer \"{self.extract_dir}\"")
        self.close()

    def connections(self):
        self.btn_extract.clicked.connect(self.extract)
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.setGeometry(500,300,800,150)
    w.show()
    sys.exit(app.exec_())