import win32com.client as win32
import os
import codecs
from PyQt5 import QtCore, QtWidgets
import sys
from pathlib import Path

sinftools_dir = os.getenv('SINFTOOLS')

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument
myRange = None

def get_last_dir():
    path = app_dir / "last_dir.txt"
    if path.exists():
        return path.read_text()

def set_last_dir(path):
    path_file = app_dir / "last_dir.txt"
    path = Path(path)
    if path.is_file():
        path = path.parent
    path_file.write_text(str(path.absolute()))

app = QtWidgets.QApplication(sys.argv)
last_dir = get_last_dir() or "C:\\"
dialog = QtWidgets.QFileDialog()
dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
dialog.setDirectory(last_dir)
if dialog.exec():
    set_last_dir(dialog.selectedFiles()[0])
    lista = [i.replace("/","\\") for i in dialog.selectedFiles()]
    valor, ok = QtWidgets.QInputDialog.getText(None, 'Quantidade de colunas','Quantidade de colunas:')
    if ok:
        n_col = int(valor)
        if len(lista)%n_col!=0:
            n_row = int(len(lista)/n_col) + 1
        else:
            n_row = int(len(lista)/n_col)
        for i in range(1,n_row +1):
            tabela = doc.Tables.Add(word.Selection.Range, 1, n_col)
            tabela.Borders.InsideLineStyle = 0
            tabela.Borders.OutsideLineStyle = 0
            for j in range(1,n_col +1):
                k = n_col*(i-1) + j-1
                if k>=len(lista):
                    break
                shape = tabela.Cell(1,j).Range.InlineShapes.AddPicture(lista[k])
                shape.LockAspectRatio = -1
                shape.Select
                tabela.Cell(1, j).Range.Paragraphs(1).Alignment = win32.constants.wdAlignParagraphCenter
                path = Path(lista[k])
                caption = shape.Range.InsertCaption(Label="Foto", Title=" - " + path.stem, Position=win32.constants.wdCaptionPositionAbove)
            tabela.Select()
            word.Selection.Collapse(0)
            word.Selection.TypeParagraph()


        # tabela = doc.Tables.Add(word.Selection.Range, n_row, n_col)
        # tabela.Borders.InsideLineStyle = 0
        # tabela.Borders.OutsideLineStyle = 0
        # for i in range(1,n_row +1):
        #     for j in range(1,n_col +1):
        #         k = n_col*(i-1) + j-1
        #         if k>=len(lista):
        #             break
        #         shape = tabela.Cell(i,j).Range.InlineShapes.AddPicture(lista[k])
        #         shape.LockAspectRatio = -1
        #         shape.Select
        #         tabela.Cell(i, j).Range.Paragraphs(1).Alignment = win32.constants.wdAlignParagraphCenter
        #         caption = shape.Range.InsertCaption(Label="Foto", Title=" - " + os.path.basename(lista[k]), Position=win32.constants.wdCaptionPositionAbove)
        #         print(shape)
sys.exit(app.exec_())