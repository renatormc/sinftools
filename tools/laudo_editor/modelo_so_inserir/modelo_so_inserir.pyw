import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import MainInterface
import os
import codecs
import json
import win32com.client as win32
import re

class Ui_MainWindow(MainInterface.Ui_MainWindow):
    def __init__(self, main):
        self.main = main
        self.setupUi(main)
        self.connections()
        with codecs.open(os.path.abspath(os.path.dirname(__file__)) + "\\..\\config.json",'r',encoding="utf-8") as arq:
            self.config = json.load(arq)
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        # self.word = win32.Dispatch('Word.Application')
        self.doc = self.word.ActiveDocument
        self.myRange = None
        self.popular_lista()

    def popular_lista(self):
        for entry in os.listdir(self.config['pasta_modelos_inserir']):
            self.lsw_modelos.addItem(entry)

    def connections(self):
        self.btn_ok.clicked.connect(self.ok_click)

    def ok_click(self):
        for i in range(int(self.edt_qtd.displayText())):
            modelo = self.config['pasta_modelos_inserir'] + '\\' +self.lsw_modelos.currentItem().text()
            current_position = self.word.Selection.Range.Start
            self.word.Selection.InsertFile(modelo)
            self.myRange = self.word.ActiveDocument.Range(Start=current_position,End = self.word.Selection.Range.Start)
        exit()     

    
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
