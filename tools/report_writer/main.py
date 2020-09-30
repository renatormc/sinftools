import click
import config
import subprocess
import os
import sys
from renderizer import Renderizer
import shutil
from pathlib import Path

def run_script(name, args=[]):
    args_ = [str(config.python_libre), str(config.app_dir / "handler/main.py"), name]
    args_ += args
    p = subprocess.run(args_)
    return p.returncode

@click.group()
@click.pass_context
def cli(ctx):
    pass



@cli.command("open-data")
def open_data():
    args = ['cmd', '/c', str(config.soffice)]
    cmd = f""
    os.system(str(config.soffice))
    #soffice .\templates\data.ods --accept=socket,host=localhost,port=2002;urp
    subprocess.Popen(args)

@cli.command("compile")
def compile():
    code = run_script("compile")
    sys.exit(code)


@cli.command("replace")
def replace():
    code = run_script("replace")
    sys.exit(code)
# @cli.command("open-data")
# @click.option('--name', '-n', default="Sem nome")
# def hello_world(name):
#     print(f"Olá {name}")


@cli.command()
def scan_pics():
    code = run_script("scan_pics")
    sys.exit(code)

@cli.command()
def start_report():
    code = run_script("read_calc")
    if code != 0:
        sys.exit(code)
    renderizer = Renderizer()
    renderizer.render("./data/calc_data.json")

@cli.command("print")
def print_():
    code = run_script("print", ["-p", "SINF"])
    if code != 0:
        sys.exit(code)

@cli.command()
def init():
    shutil.copytree(config.app_dir / "laudo", Path("./laudo"))

    

# @cli.command()
# def start_report():
#     renderer = Renderizer()
#     renderer.render()


if __name__ == '__main__':
    cli(obj={})