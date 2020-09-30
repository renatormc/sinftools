from helpers import get_pessoas_envolvidas
from helpers.excel_handler import ExcelHandler
import click
from pathlib import Path
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
    subprocess.run(['explorer', str(
        config.local_config.getprop("laudos.pasta_laudos_trabalhando"))])


@cli.command()
def pdados():
    subprocess.run(
        ['explorer', str(config.local_config.getprop("laudos.pasta_dados"))])


@cli.command()
def pics():
    eh = ExcelHandler()
    eh.connect_excel()
    eh.folder = eh.workbook_path.parent
    eh.write_pics_sheet()
   


@cli.command()
def write():
    eh = ExcelHandler()
    eh.connect_excel()
    data = eh.read_objects()
    context = data
    context['sinf'], context['rg'], context['ano'] = data['pericia'].split("/")
    context['pessoas_envolvidas'] = get_pessoas_envolvidas(context['objects'])
    model_name = (Path('.') / 'modelo.txt').read_text()
    runner = SourceFileLoader("module.name", str(
        config.app_dir / 'laudos' / model_name / "runner.py")).load_module()
    runner.run(context)
   
   


@cli.command()
def print():
    wm = WordManager()
    wm.connect()
    wm.imprimir_laudo()


if __name__ == '__main__':
    cli(obj={})
