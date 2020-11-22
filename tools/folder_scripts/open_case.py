import click
from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig
import re
import shutil

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))

sfc = SinfToolsConfig()

@click.command()
@click.argument("name")
def main(name):
    folders_create = {}
    cases_folder = Path(sfc.getprop("laudos.pasta_laudos_trabalhando"))
    if not cases_folder.exists():
        print(f"Pasta de casos \"{cases_folder}\" não existe. Cheque seus arquivos de configuração com s-config")
        return
    path = cases_folder / name
    if path.exists():
        os.system(f"explorer \"{path}\"")
        return
    else:
        res = input("Caso inexistente. Deseja criar? (S/n): ")
        res = res.strip().lower()
        if res == 'n':
            return

    folders = input("Pastas para criar (ex C-2, Notebook-3, etc):")
    folders = folders.replace(" ", "")
    if folders:
        try:
            parts = folders.split(",")
            reg = re.compile(r'(\D+)-(\d+)')
            for part in parts:
                res = reg.match(part)
                folders_create[res.group(1)] = int(res.group(2))
        except Exception as e:
            print("Formato errado", e)
            return

    path.mkdir()
    (path / "extracoes").mkdir()
    (path / "laudo").mkdir()
    (path / "midia").mkdir()
    for name, n in folders_create.items():
        for i in range(n):
            (path / f"extracoes/{name}{i+1}").mkdir()
    os.system(f"explorer \"{path}\"")


if __name__ == '__main__':
    main()
