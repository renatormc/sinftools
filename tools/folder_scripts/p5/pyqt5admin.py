import sys
import shutil
import errno
from inflection import underscore, camelize
import os
import json

script_dir = os.path.dirname(os.path.realpath(__file__))

text_help = \
"""
-new-app: 
       Cria um novo aplicativo. 

-new-app-only-code: 
       Cria um novo aplicativo sem usar o Designer, apenas código. 

-new-widget:
       Cria um novo widget.
       
-new-window:
        Cria uma nova janela descendente de QMainWindow

-new-dialog:
        Cria uma nova janela descendente de QDialog

-build:
       Converte os arquivo 'ui' e "qrc" para 'py' de todos os widgets e janelas.
"""

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

def newApp():
    nome = camelize(sys.argv[2])
    nome_ = underscore(nome)
    os.mkdir(nome_)
    os.mkdir("{}\\widgets".format(nome_))
    os.mkdir("{}\\resources".format(nome_))
    shutil.copy2("{}\\window-base\\main.ui".format(script_dir), "{0}\\{0}.ui".format(nome_))
    shutil.copy2("{}\\window-base\\build.json".format(script_dir), "{}\\build.json".format(nome_))
    shutil.copy2("{}\\window-base\\__init__.py".format(script_dir), "{}\\widgets\\__init__.py".format(nome_))
    copyanything("{}\\dev".format(script_dir), "{}\\dev".format(nome_))
    with open("{}\\window-base\\main.py".format(script_dir), "r") as infile:
        with open("{0}\\{0}.py".format(nome_), "w") as outfile:
            text = infile.read()
            text = text.replace("{{nome}}", nome).replace("{{nome_}}", nome_)
            outfile.write(text)
    with open('{}\\build.json'.format(nome_), 'r') as json_data:
        build = json.load(json_data)
    with open('{}\\build.json'.format(nome_), 'w') as json_data:
        build['widgets'].append({"name":nome_, "path":"."})
        json_data.write(json.dumps(build, ensure_ascii=False, indent=2))

def newWidget():
    nome = camelize(sys.argv[2])
    nome_ = underscore(nome)
    os.mkdir("widgets\\{}".format(nome_))
    os.mkdir("widgets\\{}\\resources".format(nome_))
    shutil.copy2("{}\\widget-base\\w.ui".format(script_dir), "widgets\\{0}\\{0}.ui".format(nome_))
    shutil.copy2("{}\\widget-base\\__init__.py".format(script_dir), "widgets\\{0}\\__init__.py".format(nome_))
    with open("{}\\widget-base\\w.py".format(script_dir), "r") as infile:
        with open("widgets\\{0}\\{0}.py".format(nome_), "w") as outfile:
            text = infile.read()
            text = text.replace("{{nome}}", nome).replace("{{nome_}}", nome_)
            outfile.write(text)
    with open('build.json', 'r') as json_data:
        build = json.load(json_data)
    with open('build.json', 'w') as json_data:
        build['widgets'].append({"name":nome_, "path":"widgets\\{}".format(nome_)})
        json_data.write(json.dumps(build, ensure_ascii=False, indent=2))

def newWidgetOnlyCode():
    copyanything("{}\\onlycode-base".format(script_dir), sys.argv[2])

def newWindow():
    nome = camelize(sys.argv[2])
    nome_ = underscore(nome)
    shutil.copy2("{}\\window-base\\main.ui".format(script_dir), "{0}.ui".format(nome_))
    with open("{}\\window-base\\main.py".format(script_dir), "r") as infile:
        with open("{0}.py".format(nome_), "w") as outfile:
            text = infile.read()
            text = text.replace("{{nome}}", nome).replace("{{nome_}}", nome_)
            outfile.write(text)
    with open('build.json', 'r') as json_data:
        build = json.load(json_data)
    with open('build.json', 'w') as json_data:
        build['widgets'].append({"name":nome_, "path":"."})
        json_data.write(json.dumps(build, ensure_ascii=False, indent=2))

def newDialog():
    nome = camelize(sys.argv[2])
    nome_ = underscore(nome)
    shutil.copy2("{}\\dialog-base\\dialog.ui".format(script_dir), "{0}.ui".format(nome_))
    with open("{}\\dialog-base\\dialog.py".format(script_dir), "r") as infile:
        with open("{0}.py".format(nome_), "w") as outfile:
            text = infile.read()
            text = text.replace("{{nome}}", nome).replace("{{nome_}}", nome_)
            outfile.write(text)
    with open('build.json', 'r') as json_data:
        build = json.load(json_data)
    with open('build.json', 'w') as json_data:
        build['widgets'].append({"name":nome_, "path":"."})
        json_data.write(json.dumps(build, ensure_ascii=False, indent=2))
        

def delWidget():
    nome = camelize(sys.argv[2])
    nome_ = underscore(nome)
    if os.path.exists("widgets\\{}".format(nome_)):
        shutil.rmtree("widgets\\{}".format(nome_))
    with open('build.json', 'r') as json_data:
        build = json.load(json_data)
    with open('build.json', 'w') as json_data:
        build['widgets'] = [w for w in build['widgets'] if w['name'] != nome_]
        json_data.write(json.dumps(build, ensure_ascii=False, indent=2))

def build():
    with open('build.json', 'r') as json_data:
        build = json.load(json_data)
    for widget in build['widgets']:
        if os.path.exists("{0}\\{1}.qrc".format(widget['path'], widget['name'])):
            os.system("%SINFTOOLS%\\Miniconda3\\Lib\\site-packages\\PyQt5\\pyrcc5.exe {0}\\{1}.qrc -o {0}\\{1}_rc.py".format(widget['path'], widget['name']))
        os.system("%SINFTOOLS%\\Miniconda3\\Lib\site-packages\\PyQt5\\pyuic5 {0}\\{1}.ui -o {0}\\ui_{1}.py".format(widget['path'], widget['name']))

funcoes = {
    "newApp": newApp,
    "build": build,
    "newWidget": newWidget,
    "delWidget": delWidget,
    "newWindow": newWindow,
    "newAppOnlyCode": newWidgetOnlyCode,
    "newDialog": newDialog
}

command = sys.argv[1]
if command == "-help" or command == "-h":
    print(text_help)
elif command == "new-app":
    funcoes['newApp']()
elif command == "new-widget":
    funcoes['newWidget']()
elif command == "build":
    funcoes['build']()
elif command == "del-widget":
    funcoes['delWidget']()
elif command == "new-window":
    funcoes['newWindow']()
elif command == "new-dialog":
    funcoes['newDialog']()
elif command == "new-app-only-code":
    funcoes['newAppOnlyCode']()     

