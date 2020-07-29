import click
from pathlib import Path
from word_manager import WordManager


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def print():
    wm = WordManager()
    wm.connect()
    wm.imprimir_laudo()


if __name__ == '__main__':
    cli(obj={})
