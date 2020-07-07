import os
from pathlib import Path
import shutil
import json
from sinf.servers import config as cf
import tempfile

sinftools_dir = Path(os.getenv("SINFTOOLS"))
app_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()

path_var = sinftools_dir / "var/iped_manager_2"
if not path_var.exists():
    os.makedirs(path_var)

output_folder = cf.output_folder
sqlite_path = cf.sqlite_path

interval_check = 10000
scripts_folder = Path(os.getenv("USERPROFILE")) / "sinf_fila_scripts"
if not scripts_folder.exists():
    os.makedirs(scripts_folder)

tempdir = Path(tempfile.gettempdir())
iped_folder = cf.iped_folder

logfile = cf.logfile

scripts_template = {
    "Processamento do IPED": {"script": "iped.bat", "process_type": "IPED"},
    "Imagem": {"script": "image.bat", "process_type": "Imagem"},
    "Outro": {"script": "other.bat", "process_type": "Outro"},
    "Sincronizar pastas": {"script": "synkdir.bat", "process_type": "Sincronização de pastas"}
}