from pathlib import Path
import json
from ctypes import windll
import subprocess

letters = ["A:\\", "B:\\", "C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\",
           "M:\\", "N:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"]


# def check_folder(path, include_path=True):
#     try:
#         path = Path(path)
#         file = path / ".sinf_mark.json"
#         if file.exists():
#             with file.open("r", encoding="utf-8") as f:
#                 marker = json.load(f)
#             if include_path:
#                 marker['path'] = str(file.parent.absolute())
#             return marker
#     except PermissionError:
#         pass

def get_markers_folder(path):
    try:
        path = Path(path)
        file = path / ".sinf_mark.json"
        with file.open("r", encoding="utf-8") as f:
            markers = json.load(f)
    except (PermissionError, FileNotFoundError, OSError):
        markers = []
    return markers


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

# def scan(path=".", data=[], max_depth=4, current_depth=0):
#     path = Path(path)
#     for entry in path.iterdir():
#         print(entry.absolute())


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


if __name__ == "__main__":
    import psutil
    ret = []
    for item in get_scannable_drives():
        info = psutil.disk_usage(item['drive'])
        percent_used = int(info.percent)
        percent_free = 100 - percent_used
        ret.append({
            'name': item['name'],
            'letter': item['drive'][:-1],
            'total': info.total,
            'used': info.used,
            'free': info.free,
            'percent_used': percent_used,
            'percent_free': percent_free
        })
    print(ret)