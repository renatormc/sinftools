import click
import PySimpleGUI as sg
from inserir_fotos2 import insert_pictures
import os
from pathlib import Path 

sinftools_dir = Path(os.getenv('SINFTOOLS'))

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

sg.theme('Light Blue 2')


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("insert-pictures")
def insert_pictures_():
    layout = [
        [sg.Text('Files', size=(8, 1)), sg.Input(key="files"), sg.FilesBrowse(initial_folder=".")],
        [sg.Text('Per row', size=(8, 1)), sg.Spin([i for i in range(1,11)], initial_value=2, key="per_row")],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Escolher arquivos', layout)
    event, values = window.read(close=True)
    window.close()
    files = values['files'].split(";")
    per_row = values['per_row']
    if event == "Submit":
        insert_pictures(files, per_row)
    # print(f'You chose filenames {values[0]} and {values[1]}')


@cli.command("insert-model")
def insert_model():
    models = [entry.name for entry in (sinftools_dir / "var/Modelos/Modelos").iterdir() if entry.name.endswith(".docx")]
    layout = [
        [sg.Listbox(values=models, size=(60, 15), key="model")],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window("Inserir modelo", layout)
    event, values = window.read(close=True)
    model = sinftools_dir / "var/Modelos/Modelos" / values['model']

if __name__ == '__main__':
    cli(obj={})
