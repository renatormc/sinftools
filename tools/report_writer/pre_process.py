from datetime import datetime


def pre_process(context):
    convert_data(context, 'data_odin', 'date')
    convert_data(context, 'data_exame', 'date')
    convert_data(context, 'data_recebimento', 'date')


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
