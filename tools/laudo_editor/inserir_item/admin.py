import sys
import shutil
import errno
import os
import json
import codecs
from inflection import underscore, camelize
from subprocess import Popen

script_dir = os.path.dirname(os.path.realpath(__file__))

text_help = \
"""
-new-widget: 
       Cria um novo widget. Recebe um único parâmetro, que é o nome da classe que irá representar o widget. 

-widget-list-update:
       Atualiza o arquivo 'widget_list.json'. Somente os widgets listados em tal arquivo ficarão disponíveis para uso.

-ui2py:
       Converte os arquivo 'ui' para 'py' de todos os widgets.
"""

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise

def getWidgetsList():
    lis = []
    for node in os.listdir("{}\\widgets".format(script_dir)):
        if node not in ['__init__.py', 'components', '__pycache__']:
            lis.append(node)
    return lis

def editWidget(wd):
    wd = camelize(wd)
    Popen(["C:\\ScriptsUFED\\extras\\Python\\Lib\\site-packages\\PyQt5\\designer.exe", "{}\\widgets\\{}\\view.ui".format(script_dir, wd)])
    # os.system("C:\\ScriptsUFED\\extras\\Python\\Lib\\site-packages\\PyQt5\\designer.exe {}\\widgets\\{}\\view.ui".format(script_dir, wd))

def editTemplate(wd):
    wd = underscore(wd)
    cmd = "start {}\\widgets\\{}\\template.docx".format(script_dir, wd)
    os.system(cmd)
   

def listUpdate():
    lis = getWidgetsList()
    with codecs.open("{}\\widget_list.json".format(script_dir),"w",'utf-8') as outfile:
        outfile.write(json.dumps(lis, ensure_ascii=False, indent=2))

def convertPrincipal():
    os.system("C:\\ScriptsUFED\\extras\\Python\\Lib\\site-packages\\PyQt5\\pyuic5 {0}\\view.ui -o {0}\\view.py".format(script_dir))
    os.system("C:\\ScriptsUFED\\extras\\Python\\Lib\\site-packages\\PyQt5\\pyrcc5 {0}\\resources.qrc -o {0}\\resources_rc.py".format(script_dir))

def convertWidget(wd):
    os.system("C:\\ScriptsUFED\\extras\\Python\\Lib\\site-packages\\PyQt5\\pyuic5 {0}\\widgets\\{1}\\view.ui -o {0}\\widgets\\{1}\\view.py".format(script_dir, wd))
    os.system("C:\\ScriptsUFED\\extras\\Python\\Lib\\site-packages\\PyQt5\\pyrcc5 {0}\\widgets\\{1}\\resources.qrc -o {0}\\widgets\\{1}\\resources_rc.py".format(script_dir, wd))

command = sys.argv[1]
if command == "help":
    print(text_help)
elif command == "new-widget":
    nome_pasta = underscore(sys.argv[2])
    copyanything("{}/widgets/components/base".format(script_dir), "{}/widgets/{}".format(script_dir, nome_pasta))

    with open("{}/widgets/{}/controller.py".format(script_dir, nome_pasta), "r") as infile:
        texto = infile.read()
    texto = texto.replace("{{widget}}", camelize(sys.argv[2]))
    with open("{}/widgets/{}/controller.py".format(script_dir, nome_pasta), "w") as outfile:
        outfile.write(texto)
    listUpdate()
elif command == "del-widget":
    shutil.rmtree("{}/widgets/{}".format(script_dir, sys.argv[2].lower()))
    listUpdate()
elif command == "widget-list-update":
    listUpdate()   
elif command == "ui2py":
    if len(sys.argv) == 2:
        convertPrincipal()
    else:
        if sys.argv[2] == "all":
            convertPrincipal()
            for item in getWidgetsList():
                convertWidget(underscore(item))
        else:
            convertWidget(underscore(sys.argv[2]))
elif command == "edit-widget":
    editWidget(sys.argv[2])
elif command == "edit-template":
    editTemplate(sys.argv[2])
