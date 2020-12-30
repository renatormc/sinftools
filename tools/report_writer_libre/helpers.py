import yaml
from pathlib import Path
import config
import shutil

def analize_pics():
    with open("data.yaml", 'r') as f:
        data = yaml.safe_load(f)
    print(data)

def copy_data_file():
    path_from = config.app_dir / "data.yaml"
    path_to = Path("./data.yaml")
    shutil.copy(path_from, path_to)