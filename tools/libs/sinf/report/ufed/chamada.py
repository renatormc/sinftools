import json
from extrator import Extrator

def getRegistro(item):
    registro = {}
    registro['contato'] = str(item.Parties).replace("From:","").replace("To:","").strip()
    registro['horario'] = str(item.TimeStamp.Value)
    registro['duracao'] = str(item.Duration.Value)
    registro['tipo'] = str(item.Type.Value)
    registro['deletado'] = str(item.Deleted)
    return registro

arquivo_saida = "chamadas.json"
#------------------------------------------------------------------------------

extrator = Extrator()
extrator.setNomeArquivo(arquivo_saida)
extrator.setFuncaoRegistro(getRegistro)
extrator.extrair(ds.Models[Call])
