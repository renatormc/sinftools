from pathlib import Path

def find_docs() -> dict:
    ret = {'capa': None, 'laudo': None, 'midia': None}
    for entry in Path(".").iterdir():
        if entry.is_file():
            if entry.name.endswith("laudo.docx"):
                ret['laudo'] = entry
            elif entry.name.endswith("capa.docx"):
                ret['capa'] = entry
            elif entry.name.endswith("midia.docx"):
                ret['midia'] = entry
    return ret