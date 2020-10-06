import yaml
from pathlib import Path
import os
import jwt
from datetime import datetime
from sinf.sinftools_config import SinfToolsConfig

stc = SinfToolsConfig()


app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))


sinfkey = os.getenv("SINFKEY")
sinfbot_token = os.getenv("SINFBOT_TOKEN")
debug = True
telegram_bot_api_port = 8003
service_port = 8002

fila_interval_check = 10000

config_folder = sinftools_dir / "var/config"
if not config_folder.exists():
    os.makedirs(config_folder)
config_path = config_folder / "servers_config.yaml"
with config_path.open("r", encoding="utf-8") as f:
    config_local = yaml.load(f, Loader=yaml.FullLoader)
sqlite_path = sinftools_dir / "var/databases/fila.db"
if not sqlite_path.parent.exists():
    os.mkdir(sqlite_path.parent)
logfile = sinftools_dir / "var/fila.log"
database_url = f"sqlite:///{sqlite_path}"

servers = {key: {'url': f"http://{value['ip']}:{value['port']}"} for key, value in config_local['servers'].items()}
timeout = 5

this_server_config = None
try:
    this_server_config = servers[config_local['server_name']]
except:
    pass

output_folder = Path(config_local['output_folder'])

def make_token():
    if sinfkey:
        now = datetime.now()
        iat = datetime.timestamp(now)
        payload = {'sub': 0, 'name': "system", 'iat': iat}
        headers = {'iat': iat}
        token = jwt.encode(payload, sinfkey,
                        headers=headers, algorithm='HS256').decode("utf-8")
        return token


SINF_TOKEN = make_token()

fila_scripts_template = {
    "Processamento do IPED": {"script": "iped.bat", "process_type": "IPED"},
    "Imagem": {"script": "image.bat", "process_type": "Imagem"},
    "Outro": {"script": "other.bat", "process_type": "Outro"},
    "Sincronizar pastas": {"script": "synkdir.bat", "process_type": "Sincronização de pastas"}
}

scripts_folder = Path(os.getenv("USERPROFILE")) / "sinf_fila_scripts"
if not scripts_folder.exists():
    os.makedirs(scripts_folder)
iped_folder = stc.getprop("servers_config.iped_folder")
iped_defaul = False
try:
    iped_folder = Path(iped_folder)
    if not iped_folder.exists():
        raise Exception("Iped folder path not found")
except:
    iped_folder = sinftools_dir / "extras/iped/iped-3.17-snapshot"
    iped_defaul = True

recycle_bin = sinftools_dir / "var/lixeira"
if not recycle_bin.exists():
    recycle_bin.mkdir()