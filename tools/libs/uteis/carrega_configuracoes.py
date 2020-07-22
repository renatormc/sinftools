import sys
import json
import os
import codecs
from uteis.formulario.input_dialog import input_dialog

def carrega_configuracoes(arquivo, op):
    with codecs.open("{}\\entrada.json".format(os.path.dirname(arquivo)), "r", "utf-8") as json_data:
        entrada = json.load(json_data)
    if op == 1:
        return entrada
    else:
        d = input_dialog("Entre os dados",entrada.keys())
        return d.resultado
     

