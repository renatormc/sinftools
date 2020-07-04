import win32com.client as win32
import os
import codecs
from PyQt5 import QtCore, QtWidgets
import sys
from pathlib import Path


word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument
myRange = None

app = QtWidgets.QApplication(sys.argv)
dialog = QtWidgets.QFileDialog()
dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
dialog.setDirectory(".")
if dialog.exec():
    lista = [i.replace("/","\\") for i in dialog.selectedFiles()]
    valor, ok = QtWidgets.QInputDialog.getText(None, 'Quantidade de colunas',
                                              'Quantidade de colunas:')
    if ok:
        n_col = int(valor)
        if len(lista)%n_col!=0:
            n_row = int(len(lista)/n_col) + 1
        else:
            n_row = int(len(lista)/n_col)
        tabela = doc.Tables.Add(word.Selection.Range, n_row, n_col)
        tabela.Borders.InsideLineStyle = 1
        tabela.Borders.OutsideLineStyle = 1
        for i in range(1,n_row +1):
            for j in range(1,n_col +1):
                k = n_col*(i-1) + j-1
                if k>=len(lista):
                    break
                tabela.Cell(i,j).Range.InlineShapes.AddPicture(lista[k])
sys.exit(app.exec_())