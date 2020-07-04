## [Imports]
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import codecs
import json
import win32com.client as win32
import re
from uteis.formulario.input_dialog import input_dialog

## [conecta ao word]
word = win32.gencache.EnsureDispatch('Word.Application')
# word = win32.Dispatch('Word.Application')
doc = word.ActiveDocument
myRange = None

## [Executa]
comp = re.compile(r'#.*?#')
lista = []
for myStoryRange in doc.StoryRanges:
    while True:
        for item in comp.findall(str(myStoryRange)):
            if item not in lista and not item.replace(" ", "")[1] == "@":
                lista.append(item)
        myStoryRange = myStoryRange.NextStoryRange
        if myStoryRange == None:
            break

d = input_dialog('Efetuar substituições',lista)

if d.resultado:
    sub = d.resultado
    for word in sub.keys():
        if sub[word] != '':
            for myStoryRange in doc.StoryRanges:
                while True:
                    myStoryRange.Find.Text = word
                    myStoryRange.Find.Replacement.Text = sub[word]
                    myStoryRange.Find.Wrap = 1 #win32.constants.wdFindContinue
                    myStoryRange.Find.Execute(Replace=2, Forward=True) #win32.constants.wdReplaceAll
                    myStoryRange = myStoryRange.NextStoryRange
                    if myStoryRange == None:
                        break
