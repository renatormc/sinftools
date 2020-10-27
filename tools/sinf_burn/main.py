import click
import subprocess
import os
from pathlib import Path
import sys
from PyInquirer import prompt
import argparse

sinftools_dir = Path(os.getenv("SINFTOOLS"))
cdburn_exe = sinftools_dir / "extras/cdburnerxp-portable-4-5-8-7128/cdbxpcmd.exe"


# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('-f', dest="folders", type=str, choices=['ask', 'one', 'many'], default='ask', help='folders')
# args = parser.parse_args()

class Burner:
    def __init__(self, disk_name, folder=".", n_copies=1, speed=12, which_folders='ask'):
        self.device = 0
        self.speed = speed
        self.n_copies = n_copies
        self.folder = Path(folder)
        self.disks = []
        self.disk_name = disk_name
        self.which_folders = which_folders
        self.get_disks()
        self.last = 0

    def get_disks(self):
        if self.which_folders == 'ask':
            choices = {
                "Gravar conteúdo da pasta corrente em um único disco": "one",
                "Gravar cada subpasta em um disco diferente": "many"
            }
            questions = [
                {
                    'type': 'list',
                    'name': 'what',
                    'message': 'Forma: ',
                    'choices': list(choices.keys())
                }
            ]
            answers = prompt(questions)
            res = choices[answers['what']]
        else:
            res = self.which_folders
        self.disks = []
        print(self.folder)
        folders = [entry for entry in self.folder.iterdir(
        ) if entry.is_dir()] if res == "many" else [self.folder]
        self.many = len(folders) > 1
        for entry in folders:
            if entry.is_dir():
                for i in range(self.n_copies):
                    self.disks.append({'subfolder': entry.name, 'copy': i + 1})

    def burn_one(self, index):
        disk = self.disks[index]
        folder = self.folder / disk['subfolder']

        name = self.disk_name.strip().replace(" ", "_")
        if self.many:
            name = f"{name}_{disk['subfolder']}"
        name = name[:16]
        print(
            f"Iniciando gravação do conteúdo da pasta \"{folder}\", cópia {disk['copy']}, nome do disco: {name}, velocidade: {self.speed}x")
        folder = self.folder / disk['subfolder']
        args = [
            str(cdburn_exe),
            '--burn-data',
            f"-device:{self.device}",
            f"-folder[\\]:{str(folder.absolute())}",
            f"-name:{name}",
            "-verify",
            f"-speed:{self.speed}",
            f"-udf:1.02"
        ]
        p = subprocess.Popen(args)
        print("\n")
        print(" ".join(args))
        p.wait()

    def burn(self):
        self.last = 0
        self.device = self.get_device()
        while True:
            index = self.what_disk()
            if index is None:
                break
            if index != self.last:
                self.last = index
            self.burn_one(index)
            self.eject()

    def eject(self):
        cmd = [str(cdburn_exe), "--eject", f"-device:{self.device}"]
        subprocess.run(cmd)

    def get_device(self):
        cmd = [str(cdburn_exe), "--list-drives"]
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        out, err = process.communicate()
        text = out.decode("CP850")
        lines = lines = [line.strip() for line in text.strip().split("\n")]
        if len(lines) == 1:
            return 0
        questions = [
            {
                'type': 'list',
                'name': 'device',
                'message': 'Selecione a gravadora: ',
                'choices': lines,
                'default': self.last
            }
        ]
        answers = prompt(questions)
        return int(answers['device'].split(":")[0].strip())

    def what_disk(self):
        # chek what is the bigger size
        max_ = 0
        for disk in self.disks:
            n = len(disk['subfolder'])
            if n > max_:
                max_ = n

        if self.many:
            choices = {
                f"Mídia {disk['subfolder'].ljust(max_, ' ')} Cópia {disk['copy']}": i for i, disk in enumerate(self.disks)}
        else:
            choices = {
                f"Cópia {disk['copy']}": i for i, disk in enumerate(self.disks)}
        choices['Finalizar'] = 'Finalizar'
        questions = [
            {
                'type': 'list',
                'name': 'what',
                'message': 'Qual disco gravar?',
                'choices': list(choices.keys())
            }
        ]
        answers = prompt(questions)
        if answers['what'] == 'Finalizar':
            return
        return choices[answers['what']]


@click.command()
@click.option('-r', '--rg', prompt='RG do caso (ex: 12345/2020)',
              help='RG do caso.')
@click.option('-s', '--speed', type=int, default=12,
              help='Velocidade de gravação.')
@click.option('-f', '--folder', default='.',
              help='Pasta contendo os arquivos a gravar.')
@click.option('-n', '--ncopies', type=int, default=2,
              help='Número de cópias.')
@click.option('-w', '--which', default="ask", help='Quais pastas')
def burn(rg, speed, folder, ncopies, which):
    try:
        rg, ano = rg.split("/")
        rg, ano = int(rg), int(ano)
        rg = f"RG{rg}.{ano}"
    except:
        print("RG fora do formato padrão")
        sys.exit(1)
    burner = Burner(disk_name=rg, folder=folder,
                    n_copies=ncopies, speed=speed, which_folders=which)
    burner.burn()
    # if many:
    #     for entry in Path(folder).iterdir():
    #         if entry.is_dir():
    #             for i in range(ncopies):
    #                 input(
    #                     f"Gravar disco {entry.name}, cópia {i+1}. Insira o disco virgem na gravadora e pressione uma tecla para prosseguir...")
    #                 burn_one(f"{rg}_{entry.name}", speed,
    #                          folder, device=device)
    # else:
    #     folder = Path(folder)
    #     subfolder = f"\{folder.name}" if subfolder else "\\"
    #     if ncopies > 1:
    #         for i in range(ncopies):
    #             input(
    #                 f"Gravar cópia {i+1}. Insira o disco virgem na gravadora e pressione uma tecla para prosseguir...")
    #             burn_one(rg, speed, folder, subfolder=subfolder)
    #     else:
    #         burn_one(rg, speed, folder, subfolder=subfolder, device=device)


if __name__ == '__main__':
    burn()
