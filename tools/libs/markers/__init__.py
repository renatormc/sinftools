from pathlib import Path
import json
from ctypes import windll
import subprocess
import os

letters = ["A:\\", "B:\\", "C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\",
           "M:\\", "N:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"]



def get_markers_folder(path):
    try:
        path = Path(path)
        file = path / ".sinf_mark.json"
        with file.open("r", encoding="utf-8") as f:
            markers = json.load(f)
    except (PermissionError, FileNotFoundError, OSError):
        markers = []
    return markers

def edit_markers(folder):
    path = Path(folder) / ".sinf_mark.json"
    os.system(f"s-np \"{path}\"")

def mark_folder(path, data):
    path = Path(path)
    file = path / ".sinf_mark.json"
    try:
        with file.open("r", encoding="utf-8") as f:
            markers = json.load(f)
    except FileNotFoundError:
        markers = []
    markers.append(data)
    with file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(markers, ensure_ascii=False, indent=4))
    # subprocess.check_call(["attrib","+H",str(file)])


def unmark_folder(path):
    path = Path(path)
    file = path / ".sinf_mark.json"
    try:
        file.unlink()
    except FileNotFoundError:
        pass


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in letters:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return drives


def get_scannable_drives():
    drives = []
    for drive in get_drives():
        markers = get_markers_folder(drive)
        if markers:
            for marker in markers:
                if marker['type'] == 'disk':
                    marker['drive'] = drive
                    drives.append(marker)
                    break
    return drives


def get_marker_of_type(markers, type_):
    for marker in markers:
        if marker['type'] == type_:
            return marker

