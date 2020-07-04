import codecs
import json

def ler_arquivo_configuracoes():
    with codecs.open(".report\\config.json", "r", "utf-8") as arq:
        data = json.load(arq)
    return data

def gravar_arquivo_configuracoes(data):
    with codecs.open(".report\\config.json", "w", "utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))

def set_tipo_telefone(tipo):
    data = ler_arquivo_configuracoes()
    data['tipo_telefone'] = tipo
    gravar_arquivo_configuracoes(data)