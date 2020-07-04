import os
import json
import codecs

dir_ = os.getenv('SINFTOOLS')
with codecs.open(f'{dir_}\\var\\config.json', 'r', 'utf-8') as arq:
    config = json.load(arq)

laudos = sorted(os.listdir(config['pasta_laudos']), key=lambda x: int(x.split(".")[0]))

for i, laudo in enumerate(laudos):
    print("{}- {}".format(i, laudo))

op = int(input("op: "))

arquivo = "{0}\\{1}\\{1}.docx".format(config['pasta_laudos'], laudos[op])
os.system("start {}".format(arquivo))

# os.system("explorer {}".format(config['pasta_laudos']))