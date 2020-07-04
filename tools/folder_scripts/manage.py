import json
import codecs
import argparse
from datetime import datetime
import os

sinftools_dir = os.getenv("SINFTOOLS")

parser = argparse.ArgumentParser(description = 'Renomeia vários arquivos de uma só vez.')
parser.add_argument('--part', action = 'store', type=int, dest = 'part',
                           default = 2, required = False, choices=[0, 1, 2],
                           help = 'Parte à incrementar')

parser.add_argument('-a --action', action = 'store', dest = 'action',
                           required = False, default='default', choices=['inc-version', 'v'],
                           help = 'Ação desejada')

parser.add_argument('-c --comment', action = 'store', dest = 'comment',
                           required = False, default='',
                           help = 'Comentário do incremento da versão')

args = parser.parse_args()
with codecs.open(f"{sinftools_dir}\\tools\\info.json", "r", "utf-8") as arq:
    dados = json.load(arq)

def default():
    pass

def version():
    print("Versão: {}".format(dados['version']))
    print("Data da última atualização: {}".format(dados['ultima_atualizacao']))
    print("Comentário: {}".format(dados['comentario']))

def inc_version():
    partes = [int(p) for p in dados['version'].split(".")]
    partes[args.part] += 1
    for i in range(args.part+1, len(partes)):
        partes[i] = 0
    dados['version'] = ".".join(str(p) for p in partes)
    dados['comentario'] = args.comment
    dados['ultima_atualizacao'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with codecs.open(f"{sinftools_dir}\\tools\\info.json", "w", "utf-8") as arq:
        arq.write(json.dumps(dados, indent=2, ensure_ascii=False))
    version()

funcoes = {
    "default": default,
    "inc-version": inc_version,
    "v": version
}

funcoes[args.action]()
