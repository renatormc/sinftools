from sinf.word_writer import settings


def set_defaults_attrib(el):
    keys = el.attrib.keys()
    if el.tag in settings.defaults.keys():
        for key, value in settings.defaults[el.tag].items():
            el.attrib[key] = el.attrib[key] if key in keys else value


def to_points(value):
    value = value.replace(" ", "")
    if value.endswith('cm'):
        w = float(value.replace("cm", ""))
        return float(w) * 0.393701 * 72
    if "/" in value:
        n, d = value.split("/")
        return (int(n) / int(d)) * settings.doc_width * 0.393701 * 72
    return (float(value) * settings.doc_width * 0.393701) * 72


def remove_br(text):
    lines = [line.strip() for line in text.split("\n")]
    return " ".join(lines)
