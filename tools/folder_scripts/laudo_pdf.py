import os
import codecs
import json
import win32com.client as win32
import pythoncom
import sys

dir_ = os.getenv('SINFTOOLS')
with codecs.open(f'{dir_}\\var\\config.json', 'r', 'utf-8') as arq:
    config = json.load(arq)

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    laudos = []
    for pasta in os.listdir(config['pasta_laudos']):
        path = os.path.join(config['pasta_laudos'], pasta)
        for item in os.listdir(path):
            if item.endswith(".docx") and not item.startswith("~") and not "controle" in item:
                laudos.append({"path": path , "arquivo": item})
    laudos = sorted(laudos, key=lambda x: x['arquivo'].split(".")[0])

    for i, item in enumerate(laudos):
        print(f"{i +1}- {item['arquivo']}")
    op = int(input("op: "))
    path =  os.path.join(laudos[op-1]['path'], laudos[op-1]['arquivo'])

clsid = "Word.Application"
clsid = pythoncom.CoCreateInstanceEx(clsid, None, pythoncom.CLSCTX_SERVER,
                                     None, (pythoncom.IID_IDispatch,))[0]

word = win32.gencache.EnsureDispatch(clsid)
word.Visible = False
doc = word.Documents.Open(path)
arquivo = os.path.basename(path)
nome_pdf = ".".join(arquivo.split(".")[:-1]) + ".pdf"
nome_abs = os.path.join(config['pasta_laudos_pdf'], nome_pdf)
doc.SaveAs(nome_abs, FileFormat = 17)
doc.Close(SaveChanges=win32.constants.wdDoNotSaveChanges)
word.Application.Quit()
print("Arquivo gerado: " + nome_abs)