from docxtpl import DocxTemplate
import os
import win32com.client as win32
script_dir = os.path.dirname(os.path.realpath(__file__))
sinftools_dir = os.getenv("SINFTOOLS")
temp_dir = f'{sinftools_dir}\\tools\\temp'

class DocxHandler:
    def __init__(self):
        if not os.path.exists(r'C:\temp'):
            os.mkdir(r'C:\temp')
        self.word = win32.gencache.EnsureDispatch('Word.Application')
        self.doc = self.word.ActiveDocument

    def copyToWord(self, template, context):
        tpl = DocxTemplate(os.path.join(script_dir, "templates", template))
        tpl.render(context)
        temp_file = os.path.join(r'C:\temp', 'temp.docx')
        tpl.save(temp_file)
        self.word.Selection.InsertFile(modelo)