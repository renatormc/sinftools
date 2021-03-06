from datetime import datetime


def pre_process(context, renderizer):
    convert_data(context, 'data_odin', 'date')
    convert_data(context, 'data_exame', 'date')
    convert_data(context, 'data_recebimento', 'date')

    for i, obj in enumerate(context['objects']):
        template = f"objetos/{obj['type']}.odt"
        name = renderizer.render_subdoc(template, obj)
        if name:
            context['objects'][i]['subdoc'] = f"[subdoc({name})]"



def convert_data(context, var, type):
    if type == 'int':
        try:
            context[var] = int(context[var])
        except:
            context[var] = 0
    if type == 'float':
        try:
            context[var] = float(context[var])
        except:
            context[var] = 0.0
    if type == 'date':
        try:
            context[var] = datetime.strptime(context[var], "%d/%m/%Y")
        except:
            pass
