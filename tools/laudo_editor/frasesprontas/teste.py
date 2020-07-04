from model import *

frase = Frase()
frase.texto = "Olá tudo bem? Como vai você, você está bem?"
frase.palavras_chave = "normal, de sempre"
session.add(frase)
session.commit()