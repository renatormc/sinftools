from pathlib import Path
import json
from sinf.servers.markers import get_markers_folder, get_drives


class FolderScanner:

    def __init__(self):
        self.max_depth = 5
        self.folders = {}
        self.current_disk_name = ""
        self.types = "*"
        self.continue_after_find = True

    def get_drives(self):
        self.drives = get_drives()

    def check_folder(self, path):
        markers = get_markers_folder(path)
        for marker in markers:
            if self.types == "*" or marker['type'] in self.types:
                self.folders[str(path)] = markers
                break

    def find_folders(self, path: Path, depth=0):
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
        self.folders = {}
        print(
            f"Iniciando vasculhamento. Profundidade máxima: {self.max_depth}")
        self.find_folders(folder)
        print(f"Vasculhando finalizado.")

    def get_drive_info(self, drive):
        markers = get_markers_folder(drive)
        for marker in markers:
            if marker['type'] == "disk":
                return marker

    def scan_drives(self):
        self.folders = {}
        self.get_drives()
        print(
            f"Iniciando vasculhamento. Profundidade máxima: {self.max_depth}")
        for drive in self.drives:
            drive_info = self.get_drive_info(drive)
            if not drive_info:
                continue
            self.current_disk_name = drive_info['name']
            print(f"Vasculhando drive {drive}...")
            self.find_folders(Path(drive))
        print(f"Vasculhando finalizado.")
