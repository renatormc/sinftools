import win32com.client as win32
import pythoncom
from pathlib import Path

class WordManager(object):

    def __init__(self):
        super().__init__()

    def connect(self):
        pythoncom.CoInitialize()
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        if not self.word:
            raise Exception("Não foi possível se conectar ao Word")
        self.doc = self.word.ActiveDocument

    def imprimir_laudo(self):
        self.doc.Application.ActivePrinter = "SINF2"
        self.doc.PrintOut(Copies=1, Pages="S2")
        self.doc.PrintOut(Copies=2, Pages="S1", ManualDuplexPrint=False)
        path = Path(self.doc.FullName).with_suffix(".pdf")
        self.doc.SaveAs2(FileName=str(path), FileFormat=17)
        


   

