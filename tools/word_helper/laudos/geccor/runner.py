from word_manager import WordManager
from helpers import converters as cv

def run(context):
    wm = WordManager()
    wm.connect()
    wm.replace("#rg#", context['rg'])
    wm.replace("#sinf#", context['sinf'])
    wm.replace("#ano#", context['ano'])
    wm.replace("#requisitante#", context['requisitante'])
    wm.replace("#ocorrencia_odin#", context['ocorrencia_odin'])
    wm.replace("#inicio_exame#", context['inicio_exame'])
    wm.replace("#data_odin#", cv.data_mes_extenso(context['data_odin']))
    wm.goto("#pessoas_envolvidas#")
    for i, pessoa in enumerate(context['pessoas_envolvidas']):
        enter = False if i == 0 else True
        wm.insert_paragraph(pessoa, indent=False, enter=enter)
    wm.goto('#objetos#')
    for name, obj in context['objects'].items():
        wm.insert_paragraph(obj['nome_laudo'], style="Título 2", enter=True)
        if obj['owner']:
            wm.insert_paragraph(f"Segundo consta este objeto está relacionado a pessoa de {obj['owner']}", enter=True)
        wm.type_enter()
        wm.render_template_insert(f"templates/objetos/{obj['type']}.docx")
        wm.insert_pictures(obj['pics'], 2)
    wm.goto('#objetos_exame#')
    for name, obj in context['objects'].items():
        wm.insert_paragraph(obj['nome_laudo'], style="Título 2", enter=True)

if __name__ == "__main__":
    run()