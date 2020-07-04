import os
from pathlib import Path
import codecs
import json
from datetime import timedelta

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = app_dir.parent.parent.absolute()

runmode = os.getenv("s_runmode") #dev, pericia, apresentacao
work_dir = os.getenv("s_work_dir")
work_dir = Path(work_dir) if work_dir else Path.cwd()
template_folder = app_dir / "templates"
static_folder = app_dir / "static"
reader_folder = app_dir / "reader"


# database =  f"sqlite:///{work_dir}/.report/db.db"


per_page = {
    "chat": 100,
    "chat_list": 200,
    "audio": 150,
    "video": 100,
    "image": 150,
    "documents": 150,
    "timeline": 2000,
    "sms": 200,
    "call": 200,
    "contact": 200,
    'file': 200
}

disregard_folders = ['.report', 'html_files']


unknow_avatar = ".report\\desconhecido.png"

# titles = {
#     'Sms': 'Mensagens SMS',
#     'Contact': "Contatos",
#     'Call': "Registros de chamadas",
#     'Chat': 'Bate-papos'
# }

port=5000

app_version = '4.8.4'

