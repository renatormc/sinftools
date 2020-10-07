from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2
import subprocess
from pathlib import Path
import os
import shutil
import config
import helpers as hp
import sys

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
apk = app_dir / "sinfpics 1.1.1.apk"

options = {
    "Instalar aplicativo no celular via adb": "install",
    "Copiar apk para a pasta corrente": "apk",
    "Copiar fotos tiradas do celular para o computador": "copy",
    "Fazer upload de fotos para o sinfweb": "upload"
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
    subprocess.run(['cmd', '/c', 's-adb', 'install', str(apk)])
elif option == "apk":
    shutil.copy(apk, Path(".") / apk.name)
elif option == "copy":
    subprocess.run(['cmd', '/c', 's-adb', 'pull',
                    '/sdcard/Pictures/sinfpics', 'sinfpics'])
elif option == "upload":
    # pericia = hp.escolher_pericia()
    # id_texto = hp.to_text_id(pericia)
    folder = Path(".")
    alias, errors = hp.check_pics(folder)
    if errors:
        print("\nHá algumas inconsistências em seus arquivos que devem ser sanadas antes de prosseguir:")
        for i, err in enumerate(errors):
            print(f"{i+1} - {err}")
        sys.exit(1)

    status_code = hp.upload_fotos(folder, id_texto)
    if status_code == 200:
        print("Upload realizado")
    elif status_code == 403:
        print(f"Você não tem permissão para fazer upload de fotos para a perícia {alias}. Possíveis causas: ")
        print("1- Você não é relator dessa perícia")
        print("2- Seu token de acesso ao sinfweb do sinftools não é válido")
