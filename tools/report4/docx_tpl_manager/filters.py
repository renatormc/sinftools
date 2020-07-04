from datetime import datetime
from docx_tpl_manager.helpers_filters import *

nome_meses = [
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]

def not_null(value):
    if value is None:
        return ""
    return value

def xxx(value):
    if value is None:
        return "XXX"
    return value


def data_completa(value):
    if not isinstance(value, datetime):
        return ""
    dia = str(value.day).rjust(2,"0")
    dia_extenso = get_extenso(value.day)
    return f"{dia} ({dia_extenso}) dias do mês de {nome_meses[value.month - 1]} do ano de {value.year} ({get_extenso(value.year)})"

def strftime_complete(date):
    if date:
        return date.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return ''


def data_mes_extenso(value):
    if not isinstance(value, datetime):
        return ""
    dia = str(value.day).rjust(2,"0")
    return f"{dia} de {nome_meses[value.month - 1]} de {value.year}"


def hora_minuto(value):
    if not isinstance(value, datetime):
        return "XXX"
    hora = str(value.hour).rjust(2,"0")
    minuto = str(value.minute).rjust(2,"0")
    return f"{hora}:{minuto}"

def dia(value):
    if not isinstance(value, datetime):
        return "XXX"
    return str(value.day).rjust(2,"0")

def dia_extenso(value):
    if not isinstance(value, datetime):
        return "XXX"
    dia = str(value.day).rjust(2,"0")
    dia_extenso = get_extenso(value.day)
    return f"{dia} ({dia_extenso})"

def mes_extenso(value):
    if not isinstance(value, datetime):
        return "XXX"
    return nome_meses[value.month-1]

if __name__ == "__main__":
    hoje = datetime.now()
    print(mes_extenso(hoje))
