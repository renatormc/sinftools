import codecs
import json

def readJson(arquivo, encoding="utf-8"):
    with codecs.open(arquivo, 'r', encoding) as arq:
        obj = json.load(arq)
    return obj

def readText(arquivo, encoding="utf-8"):
    with codecs.open(arquivo, 'r', encoding) as arq:
        text = arq.read()
    return text