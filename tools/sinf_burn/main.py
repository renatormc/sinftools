import click
import subprocess
import os
from pathlib import Path
import sys

sinftools_dir = Path(os.getenv("SINFTOOLS"))


def burn_one(name, speed, folder, subfolder="\\"):
    name = name.strip().replace(" ", "_")
    cdburn_exe = sinftools_dir / "extras/cdburnerxp-portable-4-5-8-7128/cdbxpcmd.exe"
    folder = Path(folder)
    args = [
        str(cdburn_exe),
        '--burn-data',
        '-device:0',
        f"-folder[{subfolder}]:{str(folder.absolute())}",
        f"-name:{name}",
        "-verify",
        f"-speed:{speed}"
    ]
    p = subprocess.Popen(args)
    p.wait()


@click.command()
@click.option('-r', '--rg', prompt='RG do caso (ex: 12345/2020)',
              help='RG do caso.')
@click.option('-s', '--speed', type=int, default=12,
              help='Velocidade de gravação.')
@click.option('-f', '--folder', default='.',
              help='Pasta contendo os arquivos a gravar.')
@click.option('--subfolder/--no-subfolder', default=False)
@click.option('--many/--no-many', default=False)
@click.option('-n', '--ncopies', type=int, default=1)
def burn(rg, speed, folder, subfolder, many, ncopies):
    try:
        rg, ano = rg.split("/")
        rg, ano = int(rg), int(ano)
        rg = f"RG{rg}.{ano}"
    except:
        print("RG fora do formato padrão")
        sys.exit(1)
    if many:
        for entry in Path(folder).iterdir():
            if entry.is_dir():
                for i in range(ncopies):
                    input(
                        f"Gravar disco {entry.name}, cópia {i+1}. Insira o disco virgem na gravadora e pressione uma tecla para prosseguir...")
                    burn_one(f"{rg}_{entry.name}", speed, folder)
    else:
        folder = Path(folder)
        subfolder = f"\{folder.name}" if subfolder else "\\"
        if ncopies > 1:
            for i in range(ncopies):
                input(
                    f"Gravar cópia {i+1}. Insira o disco virgem na gravadora e pressione uma tecla para prosseguir...")
                burn_one(rg, speed, folder, subfolder=subfolder)
        else:
            burn_one(rg, speed, folder, subfolder=subfolder)
   

if __name__ == '__main__':
    burn()
