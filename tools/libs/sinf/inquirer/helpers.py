from PyQt5.QtWidgets import QLabel
import codecs
import json
import os
import settings
import shutil


def get_items():
    items = []
    if os.path.exists(settings.items_folder):
        for file_ in os.listdir(settings.items_folder):
            if file_.endswith(".json"):
                items.append({"name": file_[
                    :-5], "filename": f"{settings.items_folder}\\{file_}"})
        items.sort(key=lambda k: k['name'])
    return items


def get_config(filepath):
    with codecs.open(filepath, "r", "utf-8") as f:
        data = json.load(f)
    return data


def get_list(name):
    path = os.path.join(settings.lists_folder, f"{name}.json")
    with codecs.open(path, "r", "utf-8") as f:
        data = json.load(f)
    return data


def to_points(value):
    value = value.replace(" ", "")
    if value.endswith('cm'):
        w = float(value.replace("cm", ""))
        return float(w)*0.393701*72
    if "/" in value:
        n, d = value.split("/")
        return (int(n)/int(d))*settings.doc_width*0.393701*72
    return (float(value)*settings.doc_width*0.393701)*72
    number = float(value)


def set_defaults_attrib(el):
    keys = el.attrib.keys()
    if el.tag in settings.defaults.keys():
        for key, value in settings.defaults[el.tag].items():
            el.attrib[key] = el.attrib[key] if key in keys else value


def prepare_env(reset=False):
    if reset and os.path.exists(settings.app_user_folder):
        shutil.rmtree(settings.app_user_folder)
    if not os.path.exists(settings.app_user_folder):
        shutil.copytree(os.path.join(settings.app_dir, "initial_items"), settings.app_user_folder)
    

def organize_items_rows_and_columns(items):
    rows = {}
    for item in items:
        if item['row'] in rows.keys():
            rows[item['row']].append(item)
        else:
            rows[item['row']] = [item]
    return dict(sorted(rows.items()))

