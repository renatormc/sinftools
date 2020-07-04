import os
import jinja2
import codecs
from sinf.report.emoji_replace import replaceEmoji
    
def datatempo(input):
    try:
        return input.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ''
    
def replaceEmojiChats(valor):
    return replaceEmoji(str(valor), 'html_files')

def replaceEmojiChat(valor):
    return replaceEmoji(str(valor), '.')

def baseName(valor):
    return os.path.basename(valor)
    
class Renderizador:
    def setTemplatesFolder(self, folder):
        self.loader = jinja2.FileSystemLoader(folder)
        self.env = jinja2.Environment(autoescape=True, loader=self.loader)
        self.env.filters['replaceEmojiChats'] = replaceEmojiChats
        self.env.filters['replaceEmojiChat'] = replaceEmojiChat
        self.env.filters['datetime'] = datatempo
        self.env.filters['baseName'] = baseName

    def render_template(self, template_filename, out_file, context):
        with codecs.open(out_file, 'w', 'utf-8') as arq:
            texto = self.env.get_template(template_filename).render(context)
            arq.write(texto)

if __name__ == "__main__":
    PATH = os.path.dirname(os.path.abspath(__file__))
    renderizador = Renderizador()
    renderizador.setTemplatesFolder(os.path.join(PATH, 'templates'))
    renderizador.render_template('chat.html', 'rederizado.html', {'mensagens':['mensagem 1', 'mensagem2']})
