from ui_hash_partial_dialog import Ui_HashPartialDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from pathlib import Path
import os
import config
import markers


class HashPartialDialog(QDialog):
    def __init__(self, folder):
        super(self.__class__, self).__init__()
        self.folder = Path(folder)
        self.ui = Ui_HashPartialDialog()
        self.ui.setupUi(self)
        self.connections()
        self.setWindowIcon(QIcon(f"{config.app_dir}\\resources\\marker.png"))

    def connections(self):
        self.ui.bbx_box.accepted.connect(self.accepted)
        self.ui.bbx_box.rejected.connect(self.rejected)

    def accepted(self):
       
        data = {
            'type': 'hash_partial',
            'subtype': self.ui.cbx_subtype.currentText()
        }
        markers.mark_folder(self.folder, data)
        self.close()

    def rejected(self):
        self.close()


