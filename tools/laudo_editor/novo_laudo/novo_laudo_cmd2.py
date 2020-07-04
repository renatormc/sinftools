import os
import sys
import codecs
import json
import shutil
sinftools_dir = os.getenv("SINFTOOLS")

def create_dirs(dir_, nome_base, quantidade):

    pasta = f"{dir_}\\extracoes"
    if not os.path.exists(pasta):
        os.mkdir(pasta)

    # pasta = f"{dir_}\\midia"
    # if not os.path.exists(pasta):
    #     os.mkdir(pasta)
    
    pasta = f"{dir_}\\midia\\dados"
    if not os.path.exists(pasta):
        os.mkdir(pasta)

    for i in range(quantidade):
        pasta = f"{dir_}\\extracoes\\{nome_base}{i+1}"
        os.mkdir(pasta)

    # for i in range(quantidade):
    #     pasta = f"{dir_}\\midia\\{nome_base}{i+1}"
    #     os.mkdir(pasta)
    
    for i in range(quantidade):
        pasta = f"{dir_}\\midia\\dados\\{nome_base}{i+1}"
        os.mkdir(pasta)


scriptDir = os.path.dirname(os.path.realpath(__file__))
# with codecs.open(os.path.abspath(os.path.dirname(__file__)) + "\\..\\config.json",'r',encoding="utf-8") as arq:
#     config = json.load(arq)

config = {
	"pasta_modelos": f"{sinftools_dir}\\var\\Modelos",
	"pasta_modelos_inserir": f"{sinftools_dir}\\var\\Modelos\\Modelos",
	"template_novo_laudo": f"{sinftools_dir}\\var\\template_novo_laudo"
}

with codecs.open(f"{sinftools_dir}\\var\\config.json",'r',encoding="utf-8") as arq:
    config_local = json.load(arq)

def copyanything(src, dst):   
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

nome_caso = input("Nome do caso: ")

copyanything(config['template_novo_laudo'], f"{config_local['pasta_laudos']}\\{nome_caso}")
pasta_destino = f"{config_local['pasta_laudos']}\\{nome_caso}"
dir_ = os.getenv("SINFTOOLS")
shutil.copyfile(f'{dir_}\\tools\\laudo_editor\\laudo_rapido2\\Styles.docx', f"{pasta_destino}\\{nome_caso}.docx")

while True:
    pastas = input("Criar pastas para extração e mídia?. Exemplo (Celular-5/Notebook-2): ")
    pastas = pastas.strip()

    if pastas == "":
        break
    partes = pastas.split("/")
    for parte in partes:
        nome_base, quantidade = parte.split("-")
        quantidade = int(quantidade)
        create_dirs(pasta_destino, nome_base, quantidade)

os.system(f"explorer {config_local['pasta_laudos']}\\{nome_caso}")