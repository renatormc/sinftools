
import json
import yaml
import os
from pathlib import Path
import shutil
import subprocess

sinftools_dir = Path(os.getenv("SINFTOOLS"))
config_folder = sinftools_dir / "var/config"
script_dir = Path(os.path.dirname(os.path.realpath(__file__)))


class SinfToolsConfig(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SinfToolsConfig, cls).__new__(cls)
            cls._instance.items = {}
        return cls._instance

    def refresh(self):
        self.items = {}

    def __check_file_exists(self, path):
        if not path.exists():
            shutil.copy(script_dir / "files" / path.name, path)

    def get(self, item):
        try:
            return self.items[item]
        except KeyError:
            path = config_folder / f"{item}.yaml"
            if not path.exists():
                path_from = script_dir / "files" / path.name
                try:
                    shutil.copy(path_from, path)
                except FileNotFoundError:
                    return
            with path.open("r") as file:
                self.items[item] = yaml.load(file, Loader=yaml.FullLoader)
        return self.items[item]

    def getprop(self, prop):
        try:
            parts = prop.split(".")
            value = self.get(parts[0])
            for item in parts[1:]:
                value = value[item]
            return value
        except (TypeError, KeyError):
            pass

    def edit_file(self, item):
        path = config_folder / f"{item}.yaml"
        if path.exists():
            subprocess.run(['s-npp', str(path)])
