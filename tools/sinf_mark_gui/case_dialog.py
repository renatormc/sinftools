from ui_case_dialog import Ui_CaseDialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from pathlib import Path
import os
import config
import markers


class CaseDialog(QDialog):
    def __init__(self, folder):
        super(self.__class__, self).__init__()
        self.folder = Path(folder)
        self.ui = Ui_CaseDialog()
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
                'type': 'case',
                'name': name,
                'role': self.ui.cbx_role.currentText()
            }
            markers.mark_folder(self.folder, data)
            self.close()

    def rejected(self):
        self.close()


