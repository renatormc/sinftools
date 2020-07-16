from pathlib import Path
import json
from markers import get_markers_folder, get_drives
from PyQt5.QtCore import QThread, pyqtSignal


class Scanner(QThread):

    print_message = pyqtSignal(str)
    new_marker_found = pyqtSignal(dict)


    def __init__(self):
        super(Scanner, self).__init__()
        self.max_depth = 5
        self.markers = []
        self.current_disk_name = ""
        self.types = "*"
        self.continue_after_find = True
        self.folder = None

    def get_drives(self):
        self.drives = get_drives()

    def check_folder(self, path):
        markers = get_markers_folder(path)
        for marker in markers:
            if self.types == "*" or marker['type'] in self.types:
                
                for i, m in enumerate(markers):
                    markers[i]['folder'] = str(path)
                    self.new_marker_found.emit(markers[i])
                self.markers += markers
                break

    def find_folders(self, path: Path, depth=0):
        self.print_message.emit(f"Vasculhando pasta {path}")
        if depth >= self.max_depth:
            return
        if self.check_folder(path) and not self.continue_after_find:
            return
        try:
            for entry in path.iterdir():
                if entry.is_dir() and not entry.name.startswith("$"):
                    self.find_folders(entry, depth + 1)
        except PermissionError:
            pass

    def scan_folder(self, folder):
        folder = Path(folder)
        self.markers = []
        self.print_message.emit(
            f"Iniciando vasculhamento. Profundidade máxima: {self.max_depth}")
        self.find_folders(folder)
        self.print_message.emit(f"Vasculhando finalizado.")

    def get_drive_info(self, drive):
        markers = get_markers_folder(drive)
        for marker in markers:
            if marker['type'] == "disk":
                return marker

    def scan_drives(self):
        self.markers = []
        self.get_drives()
        self.print_message.emit(f"Iniciando vasculhamento. Profundidade máxima: {self.max_depth}")
        for drive in self.drives:
            drive_info = self.get_drive_info(drive)
            if not drive_info:
                continue
            self.current_disk_name = drive_info['name']
            self.print_message.emit(f"Vasculhando drive {drive}...")
            self.find_folders(Path(drive))
        self.print_message.emit(f"Vasculhamento finalizado.")

    def run(self):
        if not self.folder:
            self.scan_drives()
        else:
            self.scan_folder(self.folder)
