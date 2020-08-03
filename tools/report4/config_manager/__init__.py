import os
from pathlib import Path
from ruamel.yaml import YAML
import codecs
import json
import uuid
import settings
import time
import shutil
from config_manager.spi_analyzer import SpiAnalyzer
from sinf.sinftools_config import SinfToolsConfig

sc = SinfToolsConfig()


class ConfigManager:
    def __init__(self):
        self.database_name = None
        self.database_type = None

  
    def read_file(self, file):
        path = Path(file)
        yaml = YAML()
        with path.open("r", encoding="utf-8") as f:
            text = f.read()
        return yaml.load(text)

    def load_database_name(self):
        with Path(".report/config/database_name.txt").open("r", encoding="utf-8") as f:
            text = f.read()
            self.database_type, self.database_name = text.split("|")

    def set_grouped(self, value):
        self.load()
        self.data['grouped'] = value
        self.save()
        self.load()

    def save(self):
        path = Path(".report/config/config.yaml")
        yaml = YAML()
        with codecs.open(path, "w", "utf-8") as f:
            yaml.dump(self.data, f)

    def get_main_config(self):
        return self.read_file(".report/config/config.yaml")


    def load(self):
        try:
            self.data = self.get_main_config()
            self.data.sources = []

            dir_ = Path(".")
            for entry in dir_.iterdir():
                if entry.is_dir() and entry.name != '.report':
                    for sub in entry.iterdir():
                        if config_manager.data['grouped']:
                            if sub.is_dir():
                                for sub2 in sub.iterdir():
                                    if sub2.is_dir() and not (sub2 / '.reportignore').exists():
                                        p = sub2 / 'config_source.yaml'
                                        if not p.exists():
                                            shutil.copy(settings.app_dir /
                                                        "config_files/config_source.yaml", p)
                                        data = self.read_file(
                                            sub2 / 'config_source.yaml')
                                        data['name'] = sub2.name
                                        data['folder'] = str(sub2)
                                        self.data.sources.append(data)
                        else:
                            if sub.is_dir() and not (sub / '.reportignore').exists():
                                data = self.read_file(
                                    sub / 'config_source.yaml')
                                data['name'] = sub.name
                                data['folder'] = str(sub)
                                self.data.sources.append(data)
            self.load_report_config()
            with Path(".report/config/file_types.json").open(encoding="utf-8") as f:
                self.file_types = json.load(f)
            self.load_database_name()
        except Exception as e:
            pass

    def is_localdb(self):
        return True if self.database_type != 'sqlite' else False

    def get_database_url(self):
        dconf = config_manager.get_db_local_config()
        if self.database_type == 'sqlite':
            return f"sqlite:///{settings.work_dir}/.report/db.db"
        if self.database_type == 'postgres':
            return f"postgresql://{dconf['user']}:{dconf['password']}@localhost/{self.database_name}"
        if self.database_type == 'mysql':
            return f"mysql://{dconf['user']}:{dconf['password']}@localhost/{self.database_name}?charset=utf8mb4"
        return f"sqlite:///{settings.work_dir}/.report/db.db"

    def generate_database_name(self, type="postgres"):
        name = f"sinf_report_{int(time.time())}"
        with Path(".report/config/database_name.txt").open("w", encoding="utf-8") as f:
            f.write(f"{type}|{name}")
        self.database_name = name

    def load_report_config(self):
        path = Path(".report/config/report_config.yaml")
        if path.exists():
            self.report_config = self.read_file(path)

    def save_report_config(self):
        path = Path(".report/config/report_config.yaml")
        yaml = YAML()
        with codecs.open(path, "w", "utf-8") as f:
            yaml.dump(self.report_config, f)

    def set_process(self, dir_, value):
        path = Path(dir_) / 'config_source.yaml'
        data = self.read_file(path)
        data['process'] = value
        yaml = YAML()
        with codecs.open(path, "w", "utf-8") as f:
            yaml.dump(data, f)
        self.load()

    def set_identifier(self, dir_, identifier):
        path = Path(dir_) / 'config_source.yaml'
        data = self.read_file(path)
        data['identifier'] = identifier
        yaml = YAML()
        with codecs.open(path, "w", "utf-8") as f:
            yaml.dump(data, f)
        self.load()

    def get_config_source_data(self, dir_):
        return self.read_file(dir_ / "config_source.yaml")


    def set_config_source_data(self, dir_, data):
        path = Path(dir_) / 'config_source.yaml'
        yaml = YAML()
        with codecs.open(path, "w", "utf-8") as f:
            yaml.dump(data, f)

    def find_source_type(self, folder: Path):
        xml_files = [entry for entry in folder.iterdir() if entry.is_file() and entry.name.lower().endswith('xml')]
        if len(xml_files) == 1:
            return ("xml_ufed", xml_files[0])
        anexos = folder / "anexos_spi"
        chats = folder / "chats_spi"
        if anexos.exists() and anexos.is_dir() and chats.exists() and chats.exists():
            return ("spi_tools", )
        if folder.name == "EXTRATOR":
            return ("extrator", )
        if (folder / "msgstore.db").exists():
            return ("sqlite",)
        if (folder / "arquivos_").exists():
            return ("files_folder", )  
        if (folder / "core.db").exists():
            return ("fbmessenger", )
        if (folder / "threads_db2").exists():
            return ("fbmessenger2", )
        if (folder / "ChatStorage.sqlite").exists():
            return ("sqlite_iphone", )
        if (folder / "HTML/WhatsApp.html").exists():
            return ("whatsapp_dr_phone", )
        return (None,)

    def ajust_config_source(self, folder: Path):
        info = self.find_source_type(folder)
        data = self.get_config_source_data(folder)
        if info[0]:
            data['source_type'] = info[0]
            if info[0] == 'xml_ufed':
                data['data_file'] = info[1].name
            elif info[0] == 'spi_tools':
                spi_analyzer = SpiAnalyzer(folder)
                data['regex_spi_tools'] = spi_analyzer.find_regex()
            elif info[0] == 'sqlite':
                pass
            elif info[0] == 'files_folder':
                pass
            elif info[0] == 'fbmessenger':
                pass
            elif info[0] == 'whatsapp_dr_phone':
                pass
        self.set_config_source_data(folder, data)


    def get_db_local_config(self):
        return sc.getprop("sinf_report_db")
        # path = Path(f"{settings.sinftools_dir}/var/config/sinf_report_db.json")
        # if not path.exists():
        #     shutil.copy(
        #         Path(settings.app_dir / "dev/sinf_report_db.json"), path)
        # if path.exists():
        #     with path.open(encoding="utf-8") as f:
        #         data = json.load(f)
        #     return data

    @property
    def sources(self):
        return self.data.sources


config_manager = ConfigManager()
config_manager.load()
config_manager.load_report_config()
try:
    config_manager.load_database_name()
except:
    pass

if __name__ == "__main__":
    os.chdir(r'C:\Users\renato\Desktop\temp\teste_report\dados')
    config_manager = ConfigManager()
    config_manager.load()
    # pprint(config_manager.data)
    config_manager.set_already_read("C1\\ufed")
    print(config_manager.data)
