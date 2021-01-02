import yaml
from pathlib import Path
import config
import shutil
from sinf_pics_helpers import NameAnalyzer

def analize_pics():
    with open("data.yaml", 'r') as f:
        data = yaml.safe_load(f)
    print(data)

def copy_data_file():
    path_from = config.app_dir / "data.yaml"
    path_to = Path("./data.yaml")
    shutil.copy(path_from, path_to)



def get_objects_from_pics(folder):
    objects = {}
    folder = Path(folder)
    if not folder.exists():
        return objects
    analyzer = NameAnalyzer()
    for entry in folder.iterdir():
        if entry.name.startswith("_"):
            continue
        res = analyzer.analise_name(entry.stem)
        if not res:
            continue
        obj = res['obj_name']
        try:
            objects[obj]['pics'].append(str(entry))
        except KeyError:
            objects[obj] = {'number': int(res['obj_number']), 'pics': [str(entry)], 'pics_files': []}
        objects[obj]['pics_files'].append(entry.name)
    items = []
    for key, value in objects.items():
        objects[key]['pics'].sort()
        items.append(
            {'name': key, 'report_name': f"Evidência {value['number']}",'number': value['number'], 'pics': value['pics'], 'pics_files': value['pics_files']})
    items.sort(key=lambda x: x['number'])
    return items