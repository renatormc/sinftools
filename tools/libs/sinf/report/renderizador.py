import os
import jinja2
import codecs
from sinf.report.emoji_replace import replaceEmoji
from numpy import nan
from math import log2
    
def datatempo(input):
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

def removeNullsNan(valor):
    valor_str = str(valor)
    if valor is None or valor == 'None' or valor == nan or valor_str == "nan":
        return ''
    return valor_str

def filesize(size):
    _suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    order = int(log2(size) / 10) if size else 0
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])


class Renderizador:
    def setTemplatesFolder(self, folder):
        self.loader = jinja2.FileSystemLoader(folder)
        self.env = jinja2.Environment(autoescape=True, loader=self.loader)
        self.env.filters['replaceEmojiChats'] = replaceEmojiChats
        self.env.filters['replaceEmojiChat'] = replaceEmojiChat
        self.env.filters['datetime'] = datatempo
        self.env.filters['removeNulls'] = removeNulls
        self.env.filters['removeNullsNan'] = removeNullsNan
        self.env.filters['filesize'] = filesize

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
