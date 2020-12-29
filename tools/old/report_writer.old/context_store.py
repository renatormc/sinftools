import json
import config
from pathlib import Path
import shutil


def start_context_files():
    try:
        config.context_file.unlink()
    except FileNotFoundError:
        pass
    if config.subdocs_temp_dir.exists():
        shutil.rmtree(config.subdocs_temp_dir)
    config.subdocs_temp_dir.mkdir()


def save_context(context):
    with config.context_file.open("w", encoding="utf-8") as f:
        f.write(json.dumps(context, ensure_ascii=False, indent=4))


def read_context():
    try:
        with config.context_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}


# def get_subdoc_context(name):
#     path = config.subdocs_context_dir / f"{name}.json"
#     try:
#         with path.open("r", encoding="utf-8") as f:
#             data = json.load(f)
#         return data
#     except FileNotFoundError:
#         return {}
