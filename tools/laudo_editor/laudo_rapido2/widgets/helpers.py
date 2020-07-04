import converters


def convert(converter, value):
    if isinstance(converter, str):
        return getattr(converters, converter)(value)
    elif isinstance(converter, list):
        return getattr(converters, converter[0])(value, *converter[1:])
    return value

class DataContext:
    def __init__(self, type_, data):
        self.type = type_
        self.data = data


def get_template_type(template_field):
    if isinstance(template_field, str):
        if template_field.endswith(".xml") or template_field.endswith('.html'):
            return 'xml'
        if template_field.endswith(".docx"):
            return 'docx'
        return None
    if isinstance(template_field, list) and len(template_field) == 2:
        return 'mix'