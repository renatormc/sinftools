import click
import config
import subprocess
import os
import sys
from app import app

def run_script(name):
    args = [str(config.python_libre), str(config.app_dir / "handler/main.py"), name]
    p = subprocess.run(args)
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

@cli.command("run-app")
def run_app():
    app.run("0.0.0.0", port=5000, debug=True)

@cli.command()
def test():
    code = run_script("main")
    sys.exit(code)


if __name__ == '__main__':
    cli(obj={})