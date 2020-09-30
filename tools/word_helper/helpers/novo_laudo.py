from styles import custom_style_2
from PyInquirer import prompt
from pathlib import Path
import os
import config
import shutil
import errno
import subprocess


def quote_items(args):
    return " ".join([f"\"{arg}\"" for arg in args])

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

def create_dirs(dir_, nome_base, quantidade):
    pasta = f"{dir_}\\extracoes"
    if not os.path.exists(pasta):
        os.mkdir(pasta)


    pasta = f"{dir_}\\midia\\dados"
    if not os.path.exists(pasta):
        os.mkdir(pasta)

    for i in range(quantidade):
        pasta = f"{dir_}\\extracoes\\{nome_base}{i+1}"
        os.mkdir(pasta)


    for i in range(quantidade):
        pasta = f"{dir_}\\midia\\dados\\{nome_base}{i+1}"
        os.mkdir(pasta)


def nova_pericia():
    pasta_modelos = config.app_dir / 'laudos'
    questions = [
        {
            'type': 'input',
            'name': 'nome_caso',
            'message': 'Nome do caso: '
        },
        {
            'type': 'list',
            'name': 'modelo',
            'message': 'Modelo:',
            'choices': [entry.name for entry in pasta_modelos.iterdir() if entry.is_dir()]
        }

    ]

    answers = prompt(questions, style=custom_style_2)

    pasta_dados =  Path(config.local_config.getprop("laudos.pasta_dados"))
    pasta_laudos_trabalhando = Path(config.local_config.getprop("laudos.pasta_laudos_trabalhando"))

    #Criar pastas de dados
    path_dados = pasta_dados / answers['nome_caso']
    path_dados.mkdir()
    (path_dados / "extracoes").mkdir(parents=True)
    (path_dados / "midia/dados").mkdir(parents=True)

    #Criar pasta de laudos
    path_laudos = pasta_laudos_trabalhando / answers['nome_caso']
    if pasta_dados == pasta_laudos_trabalhando:
        path_laudos = path_dados / "laudo"
    path_laudos.mkdir()
    shutil.copy(pasta_modelos / answers['modelo'] / "laudo.docx", path_laudos / "laudo.docx")
    shutil.copy(pasta_modelos / answers['modelo'] / "data.xlsx", path_laudos / "data.xlsx")
    for entry in (config.app_dir / "scripts").iterdir():
        shutil.copy(entry, path_laudos / entry.name)
    (path_laudos / "fotos").mkdir()
    (path_laudos / "modelo.txt").write_text(answers['modelo'])
    # copyanything(pasta_modelos / answers['modelo'], path_laudos)

    #Criar links
    if pasta_dados != pasta_laudos_trabalhando:
        args = ['cmd', '/C', 'mklink', str(path_dados / "laudo"), str(path_laudos), '/D']
        subprocess.run(args)
        args = ['cmd', '/C', 'mklink', str(path_laudos / "dados"), str(path_dados), '/D']
        subprocess.run(args)
       


    while True:
        pastas = input("Criar pastas para extração e mídia?. Exemplo (Celular-5/Notebook-2): ")
        pastas = pastas.strip()

        if pastas == "":
            break
        partes = pastas.split("/")
        for parte in partes:
            nome_base, quantidade = parte.split("-")
            quantidade = int(quantidade)
            create_dirs(path_dados, nome_base, quantidade)

    os.system(f"explorer \"{path_laudos}\"")