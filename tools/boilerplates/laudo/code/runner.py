from writer.writer import Writer
from helpers import converters as cv

def run(context):
    writer = Writer()
    writer.connect()
    writer.replace("#rg#", context['rg'])
    writer.replace("#sinf#", context['sinf'])
    writer.replace("#ano#", context['ano'])
    writer.replace("#requisitante#", context['requisitante'])
    writer.replace("#ocorrencia_odin#", context['ocorrencia_odin'])
    writer.replace("#inicio_exame#", context['inicio_exame'])
    writer.replace("#data_odin#", cv.data_mes_extenso(context['data_odin']))
    writer.goto("#pessoas_envolvidas#")
    for i, pessoa in enumerate(context['pessoas_envolvidas']):
        enter = False if i == 0 else True
        writer.insert_paragraph(pessoa, indent=False, enter=enter)
    writer.goto('#objetos#')
    for name, obj in context['objects'].items():
        writer.insert_paragraph(obj['nome_laudo'], style="Título 2", enter=True)
        if obj['owner']:
            writer.insert_paragraph(f"Segundo consta este objeto está relacionado a pessoa de {obj['owner']}", enter=True)
        writer.type_enter()
        writer.insert_doc(f"code/files/objects_templates/{obj['type']}.docx")
        writer.insert_pictures(obj['pics'], 2)
    writer.goto('#objetos_exame#')
    for name, obj in context['objects'].items():
        writer.insert_paragraph(obj['nome_laudo'], style="Título 2", enter=True)

if __name__ == "__main__":
    run()