import win32com.client as win32
import pythoncom
import os
import codecs
import sys

# word = win32.gencache.EnsureDispatch('Word.Application')
clsid = "Word.Application"
clsid = pythoncom.CoCreateInstanceEx(clsid, None, pythoncom.CLSCTX_SERVER,
                                     None, (pythoncom.IID_IDispatch,))[0]
if win32.gencache.is_readonly:
    #fix for "freezed" app: py2exe.org/index.cgi/UsingEnsureDispatch
    win32.encache.is_readonly = False
    win32.gencache.Rebuild()
    
word = win32.gencache.EnsureDispatch(clsid)
word.Visible = False
doc = word.Documents.Add()
myRange = None

extensoes = ['.jpg', '.JPG', '.PNG', '.png']


lista = [item for item in os.listdir() if os.path.splitext(item)[1] in extensoes]


n_col = int(input("Quantidade de colunas: "))
titulo = input("Título: ")
if titulo != "":
    word.Selection.Font.Name = "Arial Black"
    word.Selection.ParagraphFormat.Alignment = win32.constants.wdAlignParagraphCenter
    word.Selection.ParagraphFormat.FirstLineIndent = 0 
    word.Selection.Font.Size = 24
    word.Selection.TypeText(titulo)
    

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
        tabela.Cell(i,j).Range.InlineShapes.AddPicture(os.path.join(os.getcwd(), lista[k]))
# doc.Save()
nome_arquivo = titulo if titulo != "" else "Figuras"
if len(sys.argv) > 1:
    if sys.argv[1] == "docx":
        doc.SaveAs("{}\\{}.docx".format(os.getcwd(), nome_arquivo))
    elif sys.argv[1] == "pdf":
        doc.SaveAs("{}\\{}.pdf".format(os.getcwd(), nome_arquivo), FileFormat = 17)
        doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)
else:
    doc.SaveAs("{}\\{}.docx".format(os.getcwd(), nome_arquivo))
    doc.SaveAs("{}\\{}.pdf".format(os.getcwd(), nome_arquivo), FileFormat = 17)
    doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)

word.Application.Quit()