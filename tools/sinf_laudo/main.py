import click
import win32com.client as win32
import config
from pathlib import Path
import constants

@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("print")
def print_():
    word = win32.Dispatch('Word.Application')
    doc = word.ActiveDocument

    #imprimir laudo
    # word.ActivePrinter = config.printer_duplex_name
    # doc.PrintOut(Range=constants.wdPrintRangeOfPages, Copies=1, Pages="S1")
    word.ActivePrinter = config.printer_duplex_name
    doc.Sections(1).Range.Select()
    doc.PrintOut(Range=constants.wdPrintSelection, Copies=1)
    # word.Selection.Range.Sections(0).Range.Select()

    # #imprimir capa
    # word.ActivePrinter = config.printer_name
    # doc.PrintOut(Copies=1, Pages="S3")


    #Salvar pdf
    # path = Path(doc.FullName).with_suffix(".pdf")
    # doc.SaveAs2(FileName=str(path), FileFormat=17)



if __name__ == '__main__':
    cli(obj={})