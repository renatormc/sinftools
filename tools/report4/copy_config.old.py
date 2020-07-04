import os
import shutil
from pathlib import Path
script_dir =Path(os.path.dirname(os.path.realpath(__file__)))

dir_ = Path(".")
for entry in dir_.iterdir():
    if entry.is_dir() and entry != ".report":
        path = entry / 'config_device.yaml'
        if not path.exists():
            shutil.copy(script_dir / "config_files/config_device.yaml", path)
        for sub in entry.iterdir():
            if sub.is_dir():
                path = sub / 'config_source.yaml'
                if not path.exists():
                    shutil.copy(script_dir / "config_files/config_source.yaml", path)