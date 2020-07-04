import codecs
import json

class ConfigManager:
    def get_config_local(self):
        with codecs.open(r'C:\sinftools\var\config.json') as file_:
            config_local = json.load(file_)
        return config_local
    
    def get_config(self):
        with codecs.open(r'C:\sinftools\tools\config.json') as file_:
            config = json.load(file_)
        return config

    def get_info(self):
        with codecs.open(r'C:\sinftools\tools\info.json') as file_:
            info = json.load(file_)
        return info
# with codecs.open(r'C:\sinftools\tools\config.json') as file_:
#     config = json.load(file_)
# with codecs.open(r'C:\sinftools\tools\info.json') as file_:
#     info = json.load(file_)
# with codecs.open(r'C:\sinftools\var\config.json') as file_:
#     config_local = json.load(file_)
