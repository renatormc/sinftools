from pathlib import Path
import shutil

path_to = Path("G:/presidio")
path_from = Path.cwd()

for entry in path_from.iterdir():
    p = path_to / entry.name
    if entry.is_dir() and entry.name.lower().startswith('sinf') and not p.exists():
        for sub in p.iterdir():
            p2 = entry / sub
            if sub.is_dir() and not p2.exists():
                print(p2)
        