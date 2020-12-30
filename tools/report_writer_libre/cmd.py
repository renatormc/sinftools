import click
from helpers import *

@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("init")
# @click.option('--name', '-n', default="Sem nome")
def init():
    copy_data_file()

@cli.command("pics")
# @click.option('--name', '-n', default="Sem nome")
def pics():
    analize_pics()





if __name__ == '__main__':
    cli(obj={})