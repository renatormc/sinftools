import os
from pathlib import Path
import tempfile
import shutil
import json
import yaml
import tempfile


sinftools_dir = Path(os.getenv("SINFTOOLS"))

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

config_file = sinftools_dir / "var/iped_manager/sinf_servers.yaml"
if not config_file.exists():
    if not config_file.parent.exists():
        os.makedirs(config_file.parent)
    shutil.copy(app_dir / "config.example.yaml", config_file)

with config_file.open("r") as f:
    local_config = yaml.load(f, Loader=yaml.FullLoader)

path_var = sinftools_dir / "var/iped_manager"
sqlite_path = path_var / 'database.db'
database_url = f"sqlite:///{sqlite_path}"
SECRET_KEY = "##/q3wjP7$spG79TOjZ^rwKpXMiJAeqJnGGeI$x?"
TEMPFOLDER = Path(tempfile.gettempdir())

iped_folders = [Path(item) for item in local_config['IPED_FOLDERS']]
max_simultaneous = len(iped_folders)
