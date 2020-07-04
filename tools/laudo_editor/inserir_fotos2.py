import win32com.client as win32
import os
import codecs
from pathlib import Path

sinftools_dir = os.getenv('SINFTOOLS')

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument
myRange = None


def insert_pictures(files, n_col):
    files = [f.replace("/", "\\") for f in files]
    if len(files)%n_col!=0:
        n_row = int(len(files)/n_col) + 1
    else:
        n_row = int(len(files)/n_col)
    for i in range(1,n_row +1):
        tabela = doc.Tables.Add(word.Selection.Range, 1, n_col)
        tabela.Borders.InsideLineStyle = 0
        tabela.Borders.OutsideLineStyle = 0
        for j in range(1,n_col +1):
            k = n_col*(i-1) + j-1
            if k>=len(files):
                break
            shape = tabela.Cell(1,j).Range.InlineShapes.AddPicture(files[k])
            shape.LockAspectRatio = -1
            shape.Select
            tabela.Cell(1, j).Range.Paragraphs(1).Alignment = win32.constants.wdAlignParagraphCenter
            path = Path(files[k])
            caption = shape.Range.InsertCaption(Label="Foto", Title=" - " + path.stem, Position=win32.constants.wdCaptionPositionAbove)
        tabela.Select()
        word.Selection.Collapse(0)
        word.Selection.TypeParagraph()