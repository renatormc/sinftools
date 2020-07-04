import os
import argparse

def exec_(cmd):
    os.system(f'%SINFTOOLS%\\tools\\ADB\\adb.exe {cmd}')

parser = argparse.ArgumentParser(description='Comandos adb SINFTools.')

parser.add_argument('-a', dest='action', action='store', required=True,
                    help='Ação', choices=['extrair-sqlites-necessarios'])

args = parser.parse_args()

if args.action == "extrair-sqlites-necessarios":
    exec_("devices")
