from docxtpl import DocxTemplate
from helpers import read_sheet, write_pics_sheet, get_pessoas_envolvidas
# from sinf.word_writer.writer import Writer
from runner import run
import click
from pathlib import Path
import shutil


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def init():
    file_ = Path('code\\files\\data.xlsx').absolute()
    path = Path("data.xlsx").absolute()
    shutil.copy(file_, path)
    file_ = Path('code\\files\\laudo.docx').absolute()
    path = Path("laudo.docx").absolute()
    shutil.copy(file_, path)


@cli.command()
def pics():
    write_pics_sheet()


@cli.command()
def write():
    data = read_sheet()
    context = data
    context['sinf'], context['rg'], context['ano'] = data['pericia'].split("/")
    context['pessoas_envolvidas'] = get_pessoas_envolvidas(context['objects'])
    run(context)


if __name__ == '__main__':
    cli(obj={})
