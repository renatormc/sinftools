def strftime(date):
    if date:
        return date.strftime("%d/%m/%Y")
    else:
        return ''


def strftime_complete(date):
    if date:
        return date.strftime("%d/%m/%Y %H:%M:%S")
    else:
        return ''
