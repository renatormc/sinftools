import argparse
import os
parser = argparse.ArgumentParser(description = 'Renomeia vários arquivos de uma só vez.')
parser.add_argument('--step', action = 'store', type=int, dest = 'step',
                           default = 1, required = False,
                           help = 'Tamanho do passo, por padrão é adotado 1')

parser.add_argument('-n --name', action = 'store', dest = 'name',
                           required = True,
                           help = 'Nome para renomear os arquivos')

args = parser.parse_args()

def rename(step=1):
    i = 1
    for arq in os.listdir():
        if os.path.isfile(arq):
            filename, ext = os.path.splitext(arq)
            os.rename(arq, args.name + str(i) + ext)
            i += step

rename(step=args.step)