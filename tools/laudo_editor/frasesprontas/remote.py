import json
import codecs
import requests
import os

class Remote:
    def __init__(self):
        dir_ = os.getenv('SINFTOOLS')
        with codecs.open(f'{dir_}\\tools\\config.json') as arq:
            self.config = json.load(arq)
            
    def getFrases(self, trecho):
        url = "{}/frases-prontas/{}".format(self.config['url_frases_prontas'], trecho)
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def getFrase(self, id):
        url = "{}/frase-prontas/{}".format(self.config['url_frases_prontas'], id)
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

if __name__ == "__main__":
    remote = Remote()
    print(remote.getFrases('procurar'))