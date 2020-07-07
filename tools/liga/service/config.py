import os
from pathlib import Path
import tempfile
import shutil
import json
import tempfile
import sinf.servers.config as cf
from datetime import datetime
import jwt

sinftools_dir = Path(os.getenv("SINFTOOLS"))

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

SECRET_KEY = os.getenv("SINFKEY")

TEMPFOLDER = Path(tempfile.gettempdir())


logfile = sinftools_dir / "var/fila.log"

recycle_bin = sinftools_dir / "var/lixeira"
if not recycle_bin.exists():
    recycle_bin.mkdir()