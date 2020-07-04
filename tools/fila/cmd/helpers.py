from pathlib import Path
from ctypes import windll
import json

letters = ["A:\\", "B:\\", "C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\",
           "M:\\", "N:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"]


class DiskScanner:

    def __init__(self):
        self.max_depth = 5
        self.case_folders = []
        self.excluded_drives = ["C:\\"]

    def get_drives(self):
        self.drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in letters:
            if bitmask & 1:
                self.drives.append(letter)
            bitmask >>= 1

    def check_folder(self, path):
        try:
            file = path / ".sinf_mark.json"
            if file.exists():
                with file.open("r") as f:
                    marker = json.load(f)
                marker['path'] = str(file.parent.absolute())
                self.case_folders.append(marker)
        except PermissionError:
            pass
            
            

    def find_folders(self, path: Path, depth = 0):
            if depth >= self.max_depth:
                return
            if self.check_folder(path):
                return
            try:
                for entry in path.iterdir():
                    if entry.is_dir() and not entry.name.startswith("$"):
                        self.find_folders(entry, depth + 1)
            except PermissionError:
                pass

    def scan_drives(self):
        self.markers = []
        self.get_drives()
        for drive in self.drives:
            if drive in self.excluded_drives:
                continue
            print(f"Vasculhando drive {drive}")
            self.find_folders(Path(drive))
        self.case_folders.sort(key=lambda x: x['name'])




if __name__ == "__main__":
    analyzer = DiskScanner()
    analyzer.scan_drives()
    for folder in analyzer.case_folders:
        print(folder)
   

