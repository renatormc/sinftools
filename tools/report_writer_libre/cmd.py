import click
from helpers import *
from gui.main_window import MainWindow
import sys
from PyQt5.QtWidgets import QApplication
from uno_handler import UnoHandler


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


@cli.command("print")
def print_():
    res = input("Número de cópias, (capa,laudo,midia) (1,2,0): ").strip()
    res = res or "1,2,0"
    parts = res.split(",")
    n_capa, n_laudo, n_midia = int(parts[0]), int(parts[1]), int(parts[2])
    folder = Path("./laudo")
    handler = UnoHandler()
    handler.connect()
    for entry in folder.iterdir():
        if entry.suffix == ".odt" and "laudo" in entry.name:
            try:
                handler.open_doc(entry)
                handler.print(duplex=True)
                handler.save_pdf()
            finally:
                handler.close()


if __name__ == '__main__':
    cli(obj={})
