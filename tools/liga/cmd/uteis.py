def strfdatetime(value):
    if not value:
        return ""
    return value.strftime("%d/%m/%Y %H:%M:%S")