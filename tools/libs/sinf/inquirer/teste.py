# import win32com.client as win32
# import pythoncom

# pythoncom.CoInitialize()
# word = win32.gencache.EnsureDispatch('Word.Application')
# doc = word.ActiveDocument

# filename = 'C:\\Users\\renato\\laudos\\trabalhando\\201.18942.2019\\Fotos dos objetos\\celular (1).JPG'
# filename = 'C:/Users/renato/laudos/trabalhando/201.18942.2019/Fotos dos objetos/DSC_0005.JPG'
# filename = filename.replace("/", "\\")
# img = word.Selection.InlineShapes.AddPicture(
#             FileName=filename, LinkToFile=False, SaveWithDocument=True)

from widgets.helpers import get_template_type

print(get_template_type(["teste.docx", "teste.xml"]))