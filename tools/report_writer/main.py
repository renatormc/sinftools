from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2
import config
import subprocess
import os
import sys
from renderizer import Renderizer
import shutil
from pathlib import Path
import context_store
from pre_process import pre_process

def run_script(name, args=[]):
    args_ = [str(config.libreoffice_python), str(
        config.app_dir / "main_uno.py"), name]
    args_ += args
    p = subprocess.run(args_)
    return p.returncode

def pics():
    code = run_script("scan_pics")
    if code != 0:
        sys.exit(code)


def write():
    context_store.start_context_files()
    code = run_script("read_calc")
    if code != 0:
        sys.exit(code)

    context = context_store.read_context()
    context['contexto_local'] = config.contexto_local
    renderizer = Renderizer()
    pre_process(context, renderizer)
    renderizer.render(context)

    code = run_script("pos_process")
    if code != 0:
        sys.exit(code)



def print_():
    code = run_script("print", ["-p", config.printer_name])
    if code != 0:
        sys.exit(code)



def init():
    shutil.copy(config.app_dir / "laudo/data.ods", config.data_file)
    if not config.pics_folder.exists():
        config.pics_folder.mkdir()
    scripts_folder = config.app_dir / \
        "scripts/windows" if os.name == 'nt' else config.app_dir / "scripts/linux"
    for entry in scripts_folder.iterdir():
        if entry.is_file() and not entry.name.startswith("_"):
            shutil.copy(entry, Path(".") / entry.name)
    shutil.copy(config.app_dir / "sinf_laudo.bat", "sinf_laudo.bat")

def open_config():
    path = config.sinftools_dir / "var/config/laudos.yaml"
    os.system(f"s-np \"{path}\"")

def finish():
    sys.exit(0)


functions = {
    'Iniciar': init,
    'Escanear fotos': pics,
    'Iniciar laudo': write,
    'Imprimir': print_,
    'Configurações': open_config,
    'Sair': finish
}


questions = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'O que deseja fazer?',
        'choices': functions.keys()
    }
]


answers = prompt(questions, style=custom_style_2)
action = answers['action']
functions[action]()