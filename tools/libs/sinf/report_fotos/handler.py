from sinf.report_fotos import renderizador
import json
import codecs
import os
import shutil
script_dir = os.path.dirname(os.path.realpath(__file__))

class Handler:
    def __init__(self, itens):
        self.rend = renderizador.Renderizador()
        self.rend.setTemplatesFolder('{}\\templates'.format(script_dir))
        self.itens = itens
    
    # def carregarArquivoJson(self, path):
    #     with codecs.open(path, "r", "utf-8") as arq:
    #         self.itens = json.load(arq)

    def copiarArquivos(self):
        os.mkdir('arquivos')
        for arquivo in os.listdir():
            if os.path.isfile(arquivo):
                shutil.move(arquivo, "arquivos\\{}".format(arquivo))
               
        os.mkdir('arquivos\\anexos')
        for item in self.itens:
            for arquivo in item['arquivos']:
                shutil.copy2(arquivo, "arquivos\\anexos\\{}".format(os.path.basename(arquivo)))

    
    def render(self, arquivo_saida):
        self.rend.render_template('foo.html', arquivo_saida, {'itens': self.itens})

# if __name__ == "__main__":
#     os.chdir(r'J:\laudos\187.2017\midia')
#     handler = Handler()
#     handler.carregarArquivoJson(r'J:\laudos\187.2017\midia\links.json')
#     handler.copiarArquivos()
#     handler.render(r'J:\laudos\187.2017\midia\teste.html')

