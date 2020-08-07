import os
from pathlib import Path
import codecs
import json
import sys
from datetime import timedelta
from sinf.sinftools_config import SinfToolsConfig

sc = SinfToolsConfig()

sinftools_dir = os.getenv("SINFTOOLS")

if getattr(sys, 'frozen', False):
    app_dir = Path(os.path.dirname(sys.executable))
else:
    app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

#portable
exec_mode = os.getenv('exec_mode') or "sinf"

runmode = os.getenv("s_runmode") #dev, pericia, apresentacao
work_dir = os.getenv("s_work_dir")
work_dir = Path(work_dir) if work_dir else Path.cwd()
template_folder = app_dir / "templates"
static_folder = app_dir / "static"

p = work_dir / ".report/config/database_name.txt"
database_name, database_type = None, None
if p.exists():
    with p.open("r", encoding="utf-8") as f:
        text = f.read()
        database_type, database_name = text.split("|")
        
is_localdb = False if exec_mode == 'portable' or database_type == 'sqlite' else True

if exec_mode == 'portable' or not is_localdb:
    database = f"sqlite:///{work_dir}/.report/db.db"
else:
    dconf = sc.getprop("sinf_report_db")
    # database =  f"postgresql://{dconf['user']}:{dconf['password']}@localhost/{database_name}"
    if database_type == 'sqlite':
        database = f"sqlite:///{work_dir}/.report/db.db"
    if database_type == 'postgres':
        database= f"postgresql://{dconf['user']}:{dconf['password']}@localhost/{database_name}"
    if database_type == 'mysql':
        database = f"mysql://{dconf['user']}:{dconf['password']}@localhost/{database_name}?charset=utf8mb4"


per_page = {
    "chat": 100,
    "chat_list": 200,
    "audio": 150,
    "video": 100,
    "image": 150,
    "timeline": 2000,
    "sms": 200,
    "call": 200,
    "contact": 200,
    'file': 200
}

report_filename = "Relatório simplificado.html"


unknow_avatar = Path(".report/desconhecido.png")

# titles = {
#     'Sms': 'Mensagens SMS',
#     'Contact': "Contatos",
#     'Call': "Registros de chamadas",
#     'Chat': 'Bate-papos'
# }

port=5000

app_version = '4.8.4'

session_duration = timedelta(minutes=60)

online= True if exec_mode == "online" else False
