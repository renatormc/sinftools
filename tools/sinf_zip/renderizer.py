import os
import shutil
import jinja2
import codecs
script_dir = os.path.dirname(os.path.realpath(__file__))
    




class Renderizer:
    def __init__(self):
        self.loader = jinja2.FileSystemLoader(script_dir)
        self.env = jinja2.Environment(autoescape=True, loader=self.loader)
       

    def render_template(self, template_filename, out_file, context):
        with codecs.open(out_file, 'w', 'utf-8') as arq:
            texto = self.env.get_template(template_filename).render(context)
            arq.write(texto)


if __name__ == "__main__":
    PATH = os.path.dirname(os.path.abspath(__file__))
    renderizador = Renderizer()
    renderizador.render_template('tutorial_template.html', 'renderizado.html', {'midias': [{'name': "MIDIA 1", "files": ['dados.exe', 'dados.7z.001']}, {'name': "MIDIA 1", "files": ['dados.7z.002']}]})
