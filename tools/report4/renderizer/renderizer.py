import os
import shutil
import jinja2
import codecs
from sinf.report.emoji_replace import replaceEmoji
from numpy import nan
from math import log2
from unicodedata import normalize
import re
import urllib.request
script_dir = os.path.dirname(os.path.realpath(__file__))
    
def datetime(input):
    try:
        return input.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ''
    
def replaceEmojiChats(valor):
    return replaceEmoji(str(valor), 'html_files')

def replaceEmojiChat(valor):
    return replaceEmoji(str(valor), '.')

def removeNulls(valor):
    if valor is None or valor == 'None' or valor == nan:
        return ''
    return str(valor)

def clean_text(valor):
    aux = normalize('NFKD', valor).encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'\s+', '_', aux).lower()

def removeNullsNan(valor):
    valor_str = str(valor)
    if valor is None or valor == 'None' or valor == nan or valor_str == "nan":
        return ''
    return valor_str

def maxCaracters(valor, max):
    if len(valor) > max:
        return f"...{valor[-max:]}"
    return valor

def filesize(size):
    if not size:
        return ""
    _suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    order = int(log2(size) / 10) if size else 0
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])

def isDeleted(valor):
    return True if valor == "Deleted" else False

# def urlFile(valor):
#     return urllib.request.pathname2url(valor) if valor else None

class UrlGenerator:
    def __init__(self, base_dir):
        self.base_dir= base_dir

    def __call__(self, path):
        if path:
            path = os.path.relpath(path, self.base_dir)
            return urllib.request.pathname2url(path) if path else None


class Renderizer:
    def __init__(self, base_dir):
        self.loader = jinja2.FileSystemLoader(os.path.join(script_dir, 'templates'))
        self.env = jinja2.Environment(autoescape=True, loader=self.loader)
        self.env.filters['replaceEmojiChats'] = replaceEmojiChats
        self.env.filters['replaceEmojiChat'] = replaceEmojiChat
        self.env.filters['datetime'] = datetime
        self.env.filters['removeNulls'] = removeNulls
        self.env.filters['removeNullsNan'] = removeNullsNan
        self.env.filters['filesize'] = filesize
        self.env.filters['isDeleted'] = isDeleted
        self.env.filters['cleanText'] = clean_text
        self.env.filters['maxCaracters'] = maxCaracters
        self.env.filters['urlFile'] = UrlGenerator(base_dir)
        

    def render_template(self, template_filename, out_file, context):
        with codecs.open(out_file, 'w', 'utf-8') as arq:
            texto = self.env.get_template(template_filename).render(context)
            arq.write(texto)


    def render_template_to_string(self, template_filename, context):
        texto = self.env.get_template(template_filename).render(context)
        return texto

if __name__ == "__main__":
    PATH = os.path.dirname(os.path.abspath(__file__))
    renderizador = Renderizador()
    renderizador.setTemplatesFolder(os.path.join(PATH, 'templates'))
    renderizador.render_template('chat.html', 'rederizado.html', {'mensagens':['mensagem 1', 'mensagem2']})
