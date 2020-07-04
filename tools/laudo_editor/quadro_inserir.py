import win32com.client as win32
import os
import sys

# word = win32.gencache.EnsureDispatch('Word.Application')
word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument
myRange = None

row =2
col = 1
tabela = doc.Tables.Add(word.Selection.Range, row, col)
tabela.Cell(1,1).Select
tabela.Borders.InsideLineStyle = 1
tabela.Borders.OutsideLineStyle = 1
tabela.Rows(1).Borders(1).LineStyle = 0
tabela.Rows(1).Borders(2).LineStyle = 0
tabela.Rows(1).Borders(4).LineStyle = 0
tabela.Cell(1, 1).Range.Select
caption =  tabela.Cell(1, 1).Range.InsertCaption(Label="Quadro", Title="-?", Position =0)
tabela.Rows(1).HeadingFormat = True
tabela.Rows(1).Range.Style = doc.Styles("Legenda")