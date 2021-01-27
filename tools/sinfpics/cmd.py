from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2
import subprocess
from pathlib import Path
import os
import shutil
import config
import helpers as hp
import sys
from uteis.questions import instruct_continue

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
    instruct_continue("1- Habilite usb debug em seu aparelho\n2- Conecte o aparelho utiliando cabo usb em sua máquina\n3- Escolha \"continuar\" para prosseguir com a intalação")
    if os.name == "nt":
        subprocess.run(['cmd', '/c', 's-adb', 'install', str(apk)])
    else:
        subprocess.run(['adb', 'install', str(apk)])
elif option == "apk":
    shutil.copy(apk, Path(".") / apk.name)
    print("O arquivo apk foi copiado para sua pasta corrente. Você pode utilizá-lo para instalar o app no seu aparelho.")
elif option == "copy":
    os.system("adb pull /sdcard/Pictures/sinfpics sinfpics")
    # subprocess.run(['adb', 'pull',
    #                 '/sdcard/Pictures/sinfpics', 'sinfpics'], shell=True)
elif option == "upload":
    instruct_continue("Para que este procedimento funcione é necessário que:\n1- As fotos estejam nomeadas no padrão exigido e o terminal aberto na pasta que contém as fotos. Consulte o tutorial de como nomear fotos e objetos no sinfweb.\n2- A perícia para a qual você irá fazer o upload esteja no seu nome como relator principal ou como outro relator no sinfweb.\n3- Você já tenha o token de acesso em sua máquina, caso não tenha vá até o sinfweb para obtê-lo.")
    folder = Path(".")
    alias, errors = hp.check_pics(folder)
    if errors:
        print("\nHá algumas inconsistências em seus arquivos que devem ser sanadas antes de prosseguir:")
        for i, err in enumerate(errors):
            print(f"{i+1} - {err}")
        sys.exit(1)

    authorized = hp.check_autorization(alias)
    if not authorized:
        print(f"\nVocê não tem permissão para fazer upload de fotos para a perícia {alias}. Possíveis causas: ")
        print("1- Você não é relator dessa perícia")
        print("2- Seu token de acesso ao sinfweb do sinftools não é válido")
        sys.exit(1)

    try:
        res = hp.upload_fotos(folder, alias)
        print(f"Upload realizado com sucesso para a perícia \"{res}\"")
    except Exception as e:
        print(e)
  
   
