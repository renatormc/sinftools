import click
from pathlib import Path
import config
import shutil
import questions
from helpers import *


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def init():
    path = Path(".ipedexport")
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass
    shutil.copytree(config.app_dir / ".ipedexport", path)



@cli.command()
@click.option('--convert', is_flag=True)
def export(convert):
    res = questions.choose_filter()
    if res == "categories":
        categories2query()
    elif res == "types":
        types2query()
    elif res == "query":
        pass
    if not convert:
        run_export()



if __name__ == '__main__':
    cli(obj={})