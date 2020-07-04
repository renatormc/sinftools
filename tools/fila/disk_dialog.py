from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import config
from sinf.servers.models import *
from helpers import get_disks

class DiskDialog(QDialog):

    def __init__(self):
        super(DiskDialog, self).__init__()
        self.setup_ui()
        self.ok = False


    def setup_ui(self):
        self.setWindowTitle(f"Escolher disco")
        self.setWindowIcon(
            QIcon('{}\\resources\\icone.png'.format(config.app_dir)))
        self.main_layout = QVBoxLayout()
        self.cbx_disk = QComboBox()
        disks = get_disks()
        for disk in disks:
            self.cbx_disk.addItem(disk)
        self.main_layout.addWidget(self.cbx_disk)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok

                                           | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accepted)
        self.button_box.rejected.connect(self.rejected)
        self.main_layout.addWidget(self.button_box)
        self.setLayout(self.main_layout)



    def accepted(self):
        self.ok = True
        self.close()

    def rejected(self):
        self.ok = False
        self.close()
