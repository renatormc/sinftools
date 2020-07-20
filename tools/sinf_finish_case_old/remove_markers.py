from pathlib import Path
import markers
import sys
import json

data = []
max_depth = 5

root = Path(".")


def find_marker(folder: Path, depth=0):
    print(f"Checando pasta \"{folder}\"")
    marker = markers.check_folder(folder, include_path=False)
    if marker:
        data.append({'path': str(folder.relative_to(root)), 'marker': marker})
    markers.unmark_folder(folder)
    for entry in folder.iterdir():
        new_depth = depth + 1
        try:
            if entry.is_dir() and new_depth < max_depth:
                find_marker(entry, new_depth)
        except PermissionError:
            pass


find_marker(root)

if len(sys.argv) > 1:
    with Path(sys.argv[1]).open("w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
else:
    print(data)
print("Markers removidos")
