import codecs
import json
import os
sinftools_dir = os.getenv("SINFTOOLS")
    
def get_config(local=False):
    path = f'{sinftools_dir}\\var\\config.json' if local else f'{sinftools_dir}\\tools\\config.json'
    with codecs.open(path, 'r', 'utf-8') as file_:
        config = json.load(file_)
    return config

def get_info():
    with codecs.open(f'{sinftools_dir}\\tools\\info.json', 'r', 'utf-8') as file_:
        info = json.load(file_)
    return info

def set_config(config, local=False):
    path = f'{sinftools_dir}\\var\\config.json' if local else f'{sinftools_dir}\\tools\\config.json'
    with codecs.open(path, 'w', 'utf-8') as file_:
        file_.write(json.dumps(config, ensure_ascii=False, indent=4))

def get_key(key, local=False):
    data = get_config(local=local)
    if key in data.keys():
        return data[key]