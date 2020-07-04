import json
import codecs
from extrator import Extrator

def safestr(obj):
    if isinstance(obj, str):
        return obj
    else:
        return str(obj)

def getRegistro(item):
    registro = {}
    registro['contato'] = safestr(item.Parties).replace("From:","").replace("To:","")
    registro['corpo'] = safestr(item.Body.StringValue)
    registro['horario'] = safestr(item.TimeStamp.Value)
    registro['pasta'] = safestr(item.Folder.StringValue)
    registro['deletado'] = str(item.Deleted)
    return registro

arquivo_saida = "smss.json"
#------------------------------------------------------------------------------

extrator = Extrator()
extrator.setNomeArquivo(arquivo_saida)
extrator.setFuncaoRegistro(getRegistro)
extrator.extrair(ds.Models[SMS])
