from pyexcel_ods import get_data, save_data
from pathlib import Path
import re


class OdsHandler:

    def __init__(self):
        self.data_path = Path("./data/data.ods")
        self.pics_folder = Path("./fotos")
        self.data = None

    def read(self):
        self.data = get_data(str(self.data_path))
        # for i, item in enumerate(self.data['Variables']):
        #     print(item)

    def get_variables(self):
        vars = {}
        for i, row in enumerate(self.data['Variables']):
            if i == 0:
                continue
            n = len(row)
            if n == 2:
                vars[row[0]] = row[1]
            elif n == 1:
                vars[row[0]] = ""
        return vars

    def get_objects(self):
        objs = []
        for i, row in enumerate(self.data['Objects']):
            if i == 0:
                continue
            n = len(row)
            if n == 3:
                obj = {'name': row[0], 'type': row[1], 'pics': row[2].split(",")}
                objs.append(obj)
        return objs

    def get_context(self):
        context = self.get_variables()
        context['objects'] = self.get_objects()
        return context

    def scan_pics(self):
        self.read()
        objects = self.get_objects_from_pics()
        objects = [[f"Evidência {obj['number']}", "Celular", ",".join(
            obj['pics'])] for obj in objects]
        self.data['Objects'] = [['Nome', 'Tipo', 'Fotos']] + objects
        save_data(str(self.data_path), self.data)

    def get_objects_from_pics(self):
        objects = {}
        for entry in self.pics_folder.iterdir():
            if not entry.is_file() or not entry.suffix.lower() in ['.jpg', '.png']:
                continue
            reg = re.compile(r'((^[A-Za-z]+)(\d+)).*')
            res = reg.search(entry.name)
            obj = res.group(1).upper()
            try:
                objects[obj]['pics'].append(entry.name)
            except KeyError:
                objects[obj] = {'number': int(
                    res.group(3)), 'pics': [entry.name]}
        items = []
        for key, value in objects.items():
            objects[key]['pics'].sort()
            items.append(
                {'name': key, 'number': value['number'], 'pics': value['pics']})
        items.sort(key=lambda x: x['number'])
        return items
