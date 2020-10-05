import click
import config
import subprocess
import os
import sys
from renderizer import Renderizer
import shutil
from pathlib import Path
from ods_handler import OdsHandler

def run_script(name, args=[]):
    args_ = [str(config.libreoffice_python), str(config.app_dir / "main_uno.py"), name]
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
#     #soffice .\templates\data.ods --accept=socket,host=localhost,port=2002;urp
#     subprocess.Popen(args)

# @cli.command("compile")
# def compile():
#     code = run_script("compile")
#     sys.exit(code)


# @cli.command("replace")
# def replace():
#     code = run_script("replace")
#     sys.exit(code)
# @cli.command("open-data")
# @click.option('--name', '-n', default="Sem nome")
# def hello_world(name):
#     print(f"Olá {name}")


@cli.command()
def pics():
    handler = OdsHandler()
    handler.scan_pics()

    
@cli.command()
def write():
    handler = OdsHandler()
    handler.read()
    context = handler.get_context()
    renderizer = Renderizer()
    renderizer.render(context)

@cli.command("print")
def print_():
    code = run_script("print", ["-p", "SINF"])
    if code != 0:
        sys.exit(code)

@cli.command()
def init():
    shutil.copytree(config.app_dir / "laudo", Path("./laudo"))
    Path("./laudo/fotos").mkdir()
    scripts_folder = config.app_dir / "scripts/windows" if os.name == 'nt' else config.app_dir / "scripts/linux"
    for entry in scripts_folder.iterdir():
        if entry.is_file():
            shutil.copy(entry, Path("./laudo") / entry.name)

    

# @cli.command()
# def start_report():
#     renderer = Renderizer()
#     renderer.render()


if __name__ == '__main__':
    cli(obj={})