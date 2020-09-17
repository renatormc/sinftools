from pathlib import Path
import re

def get_pics():
    folder = Path("./fotos")
    objects = {}
    reg = re.compile(r'((^[A-Za-z]+)(\d+)).*')
    for entry in folder.iterdir():
        res = reg.search(entry.name)
        obj = res.group(1).upper()
        try:
            objects[obj]['pics'].append(str(entry))
        except KeyError:
            objects[obj] = {'number': int(res.group(3)), 'pics': [str(entry)]}
    