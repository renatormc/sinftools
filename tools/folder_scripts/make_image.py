import sys
import os
from subprocess import Popen

sinftools_dir = os.getenv("SINFTOOLS")

n = len(sys.argv)
try:
    cmd = f"s-ftkimager --list-drives"
    os.system(cmd)
    disk_number = input("\nNúmero do disco: ")
    try:
        disk_number = int(disk_number)
    except ValueError:
        exit()
    dest_file = input("Nome do arquivo de destino sem extensão: ")
    cmd = f'"{sinftools_dir}\\extras\\ftkimager\\ftkimager.exe" \\\\.\\PHYSICALDRIVE{disk_number} "{dest_file}" --e01 --verify'
    Popen(cmd)
except Exception as e:
    print(e)
input()