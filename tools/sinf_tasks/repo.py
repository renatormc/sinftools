from mongo import *
import re

def novo_objeto(nome, tipo):
    nome, tipo = nome.strip().upper(), tipo.strip().upper()
    if not nome or not tipo:
        return False
    if not TipoObjeto.objects(nome=tipo):
        tipo = TipoObjeto(nome=tipo)
        tipo.save()
    caso = re.search(r'(\w+).+', nome).group(1)
    if not Caso.objects(nome=caso):
        caso = Caso(nome=caso)
        caso.save()
    objeto = Objeto(nome=nome, caso=caso, tipo=tipo)
    objeto.save()
    return True

def get_tipos_objetos():
    return TipoObjeto.objects.order_by("nome").all()