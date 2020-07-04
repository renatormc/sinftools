import mimetypes
from pathlib import Path

def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext

# def images_from_folder(folder):
#     folder = Path(folder)
#     for entry in folder.iterdir():
#         if entry.is_file() and 