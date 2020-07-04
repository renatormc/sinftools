from docx import Document
from docxtpl import DocxTemplate, InlineImage
import win32com.client as win32
import os
script_dir = os.path.dirname(os.path.realpath(__file__))
from docx.shared import Mm

class WordHandler:
    def __init__(self):
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        self.doc = self.word.ActiveDocument
        self.temp_dir = r'C:\temp'
        self.count = 0

    def setTemplate(self, template):
        self.template = template

    def setTempDir(directory):
        self.temp_dir = directory


    def insert(self, context, imagens=[]):
         tpl = DocxTemplate(self.template)
         if imagens:
             for imagem in imagens:
                 context[imagem['tag']] = InlineImage(tpl,imagem['path'], width=Mm(imagem['width']))
         tpl.render(context)
         tpl.save("{}/temp{}.docx".format(self.temp_dir, self.count))
         self.word.Selection.InsertFile("{}/temp{}.docx".format(self.temp_dir, self.count))
         self.count += 1

if __name__ == "__main__":
    wh = WordHandler()
    wh.setTemplate("teste.docx")
    imagens = [
        {"tag":"imagem1", "path":r'C:\Users\renato\Pictures\tucano.jpg', "width":30},
        {"tag":"imagem2", "path":r'C:\Users\renato\Downloads\cofap.jpg', "width":50}
        ]
    wh.insert(context={"nome": "Renato Martins"}, imagens=imagens)