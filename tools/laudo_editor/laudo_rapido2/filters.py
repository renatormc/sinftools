from datetime import datetime
from helpers_filters import *

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


class Filters:
    @staticmethod
    def not_null(value):
        if value is None:
            return ""
        return value

    @staticmethod
    def xxx(value):
        if value is None:
            return "XXX"
        return value

    @staticmethod
    def data_completa(value):
        if not isinstance(value, datetime):
            return ""
        dia = str(value.day).rjust(2, "0")
        dia_extenso = get_extenso(value.day)
        return f"{dia} ({dia_extenso}) dias do mês de {nome_meses[value.month - 1]} do ano de {value.year} ({get_extenso(value.year)})"

    @staticmethod
    def data_mes_extenso(value):
        if not isinstance(value, datetime):
            return ""
        dia = str(value.day).rjust(2, "0")
        return f"{dia} de {nome_meses[value.month - 1]} de {value.year}"

    @staticmethod
    def data_simples(value):
        if not isinstance(value, datetime):
            return ""
        return value.strftime("%d/%m/%Y")
       

    @staticmethod
    def hora_minuto(value):
        if not isinstance(value, datetime):
            return "XXX"
        hora = str(value.hour).rjust(2, "0")
        minuto = str(value.minute).rjust(2, "0")
        return f"{hora}:{minuto}"

    @staticmethod
    def dia(value):
        if not isinstance(value, datetime):
            return "XXX"
        return str(value.day).rjust(2, "0")

    @staticmethod
    def dia_extenso(value):
        if not isinstance(value, datetime):
            return "XXX"
        dia = str(value.day).rjust(2, "0")
        dia_extenso = get_extenso(value.day)
        return f"{dia} ({dia_extenso})"

    @staticmethod
    def mes_extenso(value):
        if not isinstance(value, datetime):
            return "XXX"
        return nome_meses[value.month-1]

    @staticmethod
    def is_male(value):
        if isinstance(value, str):
            firstname = value.split()[0]
            return firstname.endswith('o')
        return False

    @staticmethod
    def get_extenso(value, female=False):
        return get_extenso(value, female=female)


filters = [getattr(Filters, func) for func in dir(Filters) if callable(
    getattr(Filters, func)) and not func.startswith("__")]
