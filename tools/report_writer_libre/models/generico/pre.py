from datetime import datetime

def convert_date(value):
    try:
        return datetime.strptime(value, "%d/%m/%Y")
    except:
        return

def pre(context):
    try:
        parts = context['pericia'].split("/")
        context['seq'], context['rg'], context['ano'] = int(parts[0]), int(parts[1]), int(parts[2])
    except:
        pass
    
    context['data_exame'] = convert_date(context['data_exame'])
    context['data_entrada'] = convert_date(context['data_entrada'])