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


@cli.command("build-query")
def build_query_():
    build_query()
    print("Query gerada no arquivo .ipedexport/query.txt")
   

@cli.command()
def export():
    build_query()
    run_export()



if __name__ == '__main__':
    cli(obj={})