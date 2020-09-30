import click
import config
import subprocess
import os
import sys
from renderizer import Renderizer
from excel_handler import ExcelHandler
from renderizer import Renderizer


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
    handler = ExcelHandler()
    handler.scan_pics()

@cli.command()
def start_report():
    renderizer = Renderizer()
    renderizer.gen_laudo()
    input()

    

# @cli.command()
# def start_report():
#     renderer = Renderizer()
#     renderer.render()


if __name__ == '__main__':
    cli(obj={})