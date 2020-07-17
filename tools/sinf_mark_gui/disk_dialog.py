from ui_disk_dialog import Ui_DiskDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from pathlib import Path
import os
import config
import markers


class DiskDialog(QDialog):
    def __init__(self, folder):
        super(self.__class__, self).__init__()
        self.folder = Path(folder)
        self.ui = Ui_DiskDialog()
        self.ui.setupUi(self)
        self.connections()
        self.setWindowIcon(QIcon(f"{config.app_dir}\\resources\\marker.png"))

    def connections(self):
        self.ui.bbx_box.accepted.connect(self.accepted)
        self.ui.bbx_box.rejected.connect(self.rejected)

    def accepted(self):
        name = self.ui.led_name.displayText().strip()
        if name and name != "":
            data = {
                'type': 'disk',
                'name': name,
                'subtype': self.ui.cbx_subtype.currentText()
            }
            markers.mark_folder(self.folder, data)
            self.close()

    def rejected(self):
        self.close()


