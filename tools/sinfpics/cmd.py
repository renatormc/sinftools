from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2
import subprocess
from pathlib import Path
import os
import shutil

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
apk = app_dir / "sinfpics 1.0.3.apk"

options = {
    "Instalar aplicativo no celular via adb": "install",
    "Copiar apk para a pasta corrente": "apk",
    "Copiar fotos tiradas do celular para o computador": "copy"
}

questions = [
    {
        'type': 'list',
        'name': 'option',
        'message': 'O que deseja fazer?',
        'choices': list(options.keys())
    },
]

answers = prompt(questions, style=custom_style_2)

option = options[answers['option']]

if option == "install":
    subprocess.run(['cmd', '/c','s-adb', 'install', str(apk)])
elif option == "apk":
    shutil.copy(apk, Path(".") / apk.name)
elif option == "copy":
    subprocess.run(['cmd', '/c','s-adb', 'pull', '/sdcard/Pictures/sinfpics', 'sinfpics'])

    