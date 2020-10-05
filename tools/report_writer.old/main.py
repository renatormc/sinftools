import click
import config
import subprocess
import os
import sys
from renderizer import Renderizer
import shutil
from pathlib import Path
import context_store


def run_script(name, args=[]):
    args_ = [str(config.libreoffice_python), str(
        config.app_dir / "main_uno.py"), name]
    args_ += args
    p = subprocess.run(args_)
    return p.returncode


@click.group()
@click.pass_context
def cli(ctx):
    pass


# @cli.command("open-data")
# def open_data():
#     args = ['cmd', '/c', str(config.soffice)]
#     cmd = f""
#     os.system(str(config.soffice))
#     # soffice .\templates\data.ods --accept=socket,host=localhost,port=2002;urp
#     subprocess.Popen(args)


# @cli.command("compile")
# def compile():
#     code = run_script("compile")
#     sys.exit(code)


# @cli.command("replace")
# def replace():
#     code = run_script("replace")
#     sys.exit(code)



@cli.command()
def pics():
    code = run_script("scan_pics")
    sys.exit(code)


@cli.command()
def write():
    context_store.start_context_files()
    code = run_script("read_calc")
    if code != 0:
        sys.exit(code)
    renderizer = Renderizer()
    renderizer.render()


@cli.command("print")
def print_():
    code = run_script("print", ["-p", config.printer_name])
    if code != 0:
        sys.exit(code)


@cli.command()
def init():
    shutil.copy(config.app_dir / "laudo/data.ods", config.data_file)
    if not config.pics_folder.exists():
        config.pics_folder.mkdir()
    scripts_folder = config.app_dir / \
        "scripts/windows" if os.name == 'nt' else config.app_dir / "scripts/linux"
    for entry in scripts_folder.iterdir():
        if entry.is_file():
            shutil.copy(entry, Path(".") / entry.name)


# @cli.command()
# def start_report():
#     renderer = Renderizer()
#     renderer.render()

if __name__ == '__main__':
    cli(obj={})
