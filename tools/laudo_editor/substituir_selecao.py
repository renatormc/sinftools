import win32com.client as win32
# from win32com.client import makepy
import os
import sys
import re
from formulario.input_dialog import input_dialog

# makepy.main ()
word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument

def substituir_em_range(range):
        comp = re.compile(r'#.*?#')
        lista = []
        for par in range.Paragraphs:
            for item in comp.findall(str(par)):
                if item not in lista and not item.replace(" ", "")[1] == "@":
                    lista.append(item)
        d = input_dialog('Efetuar substituições', lista)
        if d.resultado:
            sub = d.resultado
            for palavra in sub.keys():
                if sub[palavra] != '':
                    range.Find.Text = palavra
                    range.Find.Replacement.Text = sub[palavra]
                    range.Find.Execute(Replace=win32.constants.wdReplaceAll, Forward=True)

current_position = word.Selection.Range.Start
substituir_em_range(word.Selection)