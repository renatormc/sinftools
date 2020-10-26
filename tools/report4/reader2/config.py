import os
from pathlib import Path


app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

work_dir = Path.cwd()
unknow_avatar = ".report/desconhecido.png"
port = 5000