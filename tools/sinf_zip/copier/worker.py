from PyQt5.QtCore import QThread, pyqtSignal
import os
from confirm_dialog import ConfirmDialog
import time


class Worker(QThread):

    update_progress = pyqtSignal(int, int)
    show_message = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.chunk_size = 1000
        self.nfiles = len(self.parent.config.keys()) + 1
        self.n_copied_files = 0
        self.tempdir = None

    def wait_for_midia(self, midia):
        self.show_message.emit(f"INSIRA MÍDIA {midia}")
        self.parent.midia_found = False
        file = f"{self.parent.drive}\\.sinf\\current_midia.txt"
        while True:
            
            if os.path.exists(file):
                with open(file, "r") as f:
                    value = int(f.read())
                if value == midia:
                    self.show_message.emit("")
                    return True
                    break
            time.sleep(0.1)
        self.show_message.emit("")
        return False

    def run(self):
        #for file_ in self.config['files']:
        self.n_copied_files = 0
        self.nfiles = len(self.parent.config.keys()) + 1
        for key, files in self.parent.config.items():
            key = int(key) if isinstance(key, str) else key
            current_midia = self.parent.get_current_midia()
            if not current_midia or current_midia != key:
                res = self.wait_for_midia(key)
                if not res:
                    return
            for file_ in files:
                with open(os.path.join(self.parent.drive, ".sinf", file_), "rb") as f:
                    path = os.path.join(self.parent.tempdir, os.path.basename(file_))
                    if os.path.exists(path):
                        os.remove(path)
                    with open(path, "wb") as fout:
                        f.seek(0, 2)
                        filesize = f.tell()
                        f.seek(0, 0)
                        while True:
                            data = f.read(self.chunk_size)
                            p = f.tell()/filesize
                            individual_progress = int(p*100)
                            general_progress = int(((self.n_copied_files + p)/self.nfiles)*100)
                            self.update_progress.emit(general_progress, individual_progress)
                            if not data:
                                break
                            fout.write(data)
                self.n_copied_files += 1
        self.finished.emit()
            