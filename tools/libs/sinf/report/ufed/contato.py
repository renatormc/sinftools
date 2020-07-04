import json
from extrator import *

def safestr(obj):
    if isinstance(obj, str):
        return obj
    else:
        return str(obj)

def getRegistro(item):
    registro = {}
    registro['nome'] = safestr(item.Name.Value)
    Entradas =""
    for entrada in item.Entries:
        Entradas = Entradas + str(entrada) + "\n"
    registro['entradas'] = Entradas
    registro['origem'] = str(item.Source.Value)
    registro['deletado'] = str(item.Deleted)
    return registro

arquivo_saida = "contatos.json"
#------------------------------------------------------------------------------

extrator = Extrator()
extrator.setNomeArquivo(arquivo_saida)
extrator.setFuncaoRegistro(getRegistro)
extrator.extrair(ds.Models[Contact])
