import os
from pathlib import Path
import shutil
import yaml

sinftools_dir = Path(os.getenv("SINFTOOLS"))
app_dir = Path(os.path.dirname(os.path.realpath(__file__))).absolute()

config_folder = sinftools_dir / "var/fila"
if not config_folder.exists():
    os.makedirs(config_folder)

config_path = config_folder / "servers_config.yaml"
if not config_path.exists():
    shutil.copy(app_dir / "servers_config.example.yaml", config_path)

with config_path.open("r", encoding="utf-8") as f:
    config_local = yaml.load(f, Loader=yaml.FullLoader)

sqlite_path = config_folder / 'database.db'
database_url = f"sqlite:///{sqlite_path}"
# database_url = config_local['database_url']
iped_folder = Path(config_local['iped_folder'])
output_folder = Path(config_local['output_folder'])
ftkimager = sinftools_dir / "extras/ftkimager/ftkimager.exe"

telegram_sender_url = "http://10.129.3.132:8002"

logfile = sinftools_dir / "var/fila.log"

sinf_secret = os.getenv("SINF_SECRET")

# connection_files_dir = sinftools_dir / "tools/fila/cmd/connection_files"

servers = {key: {'url': f"http://{value['ip']}:{value['port']}"} for key, value in config_local['servers'].items()}

# servers = {
#     # 'batman': {
#     #     'url': "http://10.129.3.128:8002",
#     #     'connection_file': str(connection_files_dir / "batman.rdp")
#     # },
#     'batman': {
#         'url': "http://192.168.207.129:8002",
#         'connection_file': str(connection_files_dir / "batman.rdp")
#     },
#     'superman': {
#         'url': "http://10.129.3.132:8002",
#         'connection_file': str(connection_files_dir / "superman.rdp")
#     },
#     'mulher_maravilha': {
#         'url': "http://10.129.3.120:8002",
#         'connection_file': str(connection_files_dir / "mulher_maravilha.rdp")
#     }
# }

timeout = 5

this_server_config = None
try:
    this_server_config = servers[config_local['server_name']]
except:
    pass
