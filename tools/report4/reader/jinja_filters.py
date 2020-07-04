import json
import pathlib
from helpers import filesize2human

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


def filename_max(valor):
    if valor and len(valor) > 30:
        return valor[:15] + "..."
    return valor


def force_scape_json(value):
    return json.dumps(value).replace("\"", "&quot;")


def file_ext(value):
    return pathlib.Path(value).suffix

  

def filesize(size):
    try:
        return filesize2human(size)
    except:
        return None

def is_deleted(value):
    return True if value == "Deleted" else False