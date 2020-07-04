import sys
import codecs
import json
import shutil
import os

dir_ = os.getenv('SINFTOOLS')
with codecs.open(f'{dir_}\\var\\config.json', 'r', 'utf-8') as arq:
    config = json.load(arq)
path = sys.argv[1]
file_ = sys.argv[2]
try:
    shutil.copy2(os.path.join(path, file_), os.path.join(config['pasta_revisao'], file_))
    print("Arquivo enviado para a pasta de revisão. Pressiona alguma tecla para sair.")
except:
    print("Houve um erro. Talvez você não esteja logado no servidor de arquivos.")
input()

