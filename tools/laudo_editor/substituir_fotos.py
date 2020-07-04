import win32com.client as win32
import os
import sys
import re
# from uteis.formulario.input_dialog import input_dialog

word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument

def substituir_em_range(range):
        comp = re.compile(r'#.*?#')
        lista = []
        for par in range.Paragraphs:
            for item in comp.findall(str(par)):
                if item not in lista and item.replace(" ", "")[1] == "@":
                    lista.append(item)
        # d = input_dialog('Efetuar substituições', lista)
        # if d.resultado:
        #     sub = d.resultado
        #     for word in sub.keys():
        #         if sub[word] != '':
        #             range.Find.Text = word
        #             range.Find.Replacement.Text = sub[word]
        #             range.Find.Execute(Replace=2, Forward=True)

current_position = word.Selection.Range.Start
substituir_em_range(word.Selection)