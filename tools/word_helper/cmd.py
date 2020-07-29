from helpers import read_sheet, write_pics_sheet, get_pessoas_envolvidas
import click
from pathlib import Path
import shutil
import subprocess
import config
from importlib.machinery import SourceFileLoader
from word_manager import WordManager

from helpers.novo_laudo import nova_pericia


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def nova():
    nova_pericia()

@cli.command()
def plaudos():
    subprocess.run(['explorer', str(config.local_config.getprop("laudos.pasta_laudos_trabalhando"))])

@cli.command()
def pdados():
    subprocess.run(['explorer', str(config.local_config.getprop("laudos.pasta_dados"))])

@cli.command()
def pics():
    write_pics_sheet()


@cli.command()
def write():
    data = read_sheet()
    context = data
    context['sinf'], context['rg'], context['ano'] = data['pericia'].split("/")
    context['pessoas_envolvidas'] = get_pessoas_envolvidas(context['objects'])
    runner = SourceFileLoader("module.name", "./runner.py").load_module()
    runner.run(context)

@cli.command()
def print():
    wm = WordManager()
    wm.connect()
    wm.imprimir_laudo()


if __name__ == '__main__':
    cli(obj={})
