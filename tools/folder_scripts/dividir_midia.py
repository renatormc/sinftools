import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Divide arquivos em pastas de forma que caiba em CDs ou DVDs')
parser.add_argument('-m', dest='midia', action='store', required = True,  choices=['cd', 'dvd'], help='Mídia a ser utilizada.')
parser.add_argument('-n', dest='nome', action='store', help='Nome base', required=True)
args = parser.parse_args()

if args.midia == "dvd":
    max_size = 4700000000
elif args.midia == "cd":
    max_size = 734003200

lista = os.listdir()

total_size = 0
n_folders = 1
current_folder = "{}{}".format(args.nome, n_folders)
os.mkdir(current_folder)
for arq in lista:
    size = os.path.getsize(arq)
    print(total_size, max_size)
    if (total_size + size) > max_size:
        total_size = 0
        n_folders += 1
        current_folder = "{}{}".format(args.nome, n_folders)
        os.mkdir(current_folder)
    shutil.move(arq, "{}\\{}".format(current_folder, arq))
    total_size += size
