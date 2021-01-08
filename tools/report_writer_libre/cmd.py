import click
from helpers import *
from gui.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("laudo")
def laudo():
    app = QApplication(sys.argv)
    w = MainWindow(".")
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    cli(obj={})
