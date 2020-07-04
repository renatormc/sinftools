import os
import shutil
import io
import sys
from PyInquirer import style_from_dict, Token, prompt, Separator
import socket
from string import Template
import codecs
import time
import settings
from config_manager import config_manager
from models import *
from database import db_session
from helpers import *
import multiprocessing
import constants
from subprocess import Popen


script_dir = os.path.dirname(os.path.realpath(__file__))

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def instruct_continue(message):
    print("\n")
    if message:
        print(message)
        print("\n")
    questions = [
        {
            'type': 'list',
            'message': "O que deseja fazer?",
            'name': 'action',
            'pageSize': 3,
            'choices': [
                'Continuar',
                'Cancelar'
            ]
        }
    ]
    res = prompt(questions, style=style)
    if res['action'] == 'Cancelar':
        print("Cancelar")
        sys.exit()


def askfor_update():    
    questions = [
        {
            'type': 'list',
            'message': "Antes de iniciar um novo projeto é recomendado que atualize o sinftools. O que deseja fazer?",
            'name': 'action',
            'pageSize': 3,
            'choices': [
                'Atualizar',
                'Continuar sem atualizar (não recomendado)'
            ]
        }
    ]
    res = prompt(questions, style=style)
    if res['action'] == 'Atualizar':
        os.system("s-update")
        sys.exit()

def show_options_cancel(message, options, cancel_option=False):
    if cancel_option:
        options.append("Cancelar")
    questions = [
        {
            'type': 'list',
            'message': message,
            'name': 'action',
            'pageSize': 3,
            'choices': options
        }
    ]
    res = prompt(questions, style=style)
    if cancel_option and res['action'] == 'Cancelar':
        sys.exit()
    return res['action']


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben
    

def copy_config_files(overwrite=False):
    dir_ = Path(".")
    for entry in dir_.iterdir():
        if entry.is_dir() and entry.name != ".report":
            for sub in entry.iterdir():
                if config_manager.data['grouped']:
                    if sub.is_dir():
                        for sub2 in sub.iterdir():
                            if sub2.is_dir():
                                path = sub2 / 'config_source.yaml'
                                if not path.exists() or overwrite:
                                    shutil.copy(settings.app_dir /
                                                "config_files/config_source.yaml", path)
                                    # os.system(f"attrib +h \"{path}\"" )
                                    config_manager.ajust_config_source(sub2)
                else:
                    if sub.is_dir():
                        path = sub / 'config_source.yaml'
                        if not path.exists() or overwrite:
                            shutil.copy(settings.app_dir /
                                        "config_files/config_source.yaml", path)
                            # os.system(f"attrib +h \"{path}\"" )
                            config_manager.ajust_config_source(sub)


def copy2_verbose(src, dst):
    print('Copying {0}'.format(src))
    shutil.copy2(src, dst)


def copy_folder(source, destination):
    shutil.copytree(source, destination, copy_function=copy2_verbose)


def update_sources():
    sources = [(source['identifier'], source)
               for source in config_manager.data.sources]
    ids = [el[0] for el in sources if el[0] is not None]
    if ids:
        read_sources_orphan = db_session.query(ReadSource).filter(
            ~ReadSource.id.in_(ids)).all()
        if read_sources_orphan:
            for rs in read_sources_orphan:
                print(f"Deletando fonte de dados orfã '{rs.folder}'")
                db_session.delete(rs)
            db_session.commit()
    for id, source in sources:
        rs = db_session.query(ReadSource).get(id) if id else None
        if not rs:
            print(source['folder'])
            rs = ReadSource()
            config_manager.set_process(source['folder'], True)
            # config_manager.ajust_config_source(Path(source['folder']))
        rs.folder = source['folder']
        rs.device = get_read_source_device(rs)
        rs.data_file = source['data_file']
        rs.source_type = source['source_type']
        rs.process = source['process']
        rs.regex_spi_tools = source['regex_spi_tools']
        rs.chat_source = source['chat_source'] or "-"
        db_session.add(rs)
        db_session.commit()
        config_manager.set_identifier(source['folder'], rs.id)
    delete_orphan_devices()


def delete_thumbs_folders():
    for item in Path(".").glob('**/*/*/sinf_thumbs'):
        if item.is_dir():
            shutil.rmtree(item)

def delete_reports():
    for item in Path(".").glob('**/*/html_files'):
        if item.is_dir():
            shutil.rmtree(item)
    for item in Path(".").glob(f'**/*/{constants.HTML_REPORT_NAME}'):
        if item.is_file():
            os.remove(item)


def reset(dbtype):
    if os.path.exists('.report'):
        shutil.rmtree('.report')
    if os.path.exists('html_files'):
        shutil.rmtree(('html_files'))
    if os.path.exists(constants.ANALYZER_EXE_NAME):
        os.remove(constants.ANALYZER_EXE_NAME)
    if os.path.exists(constants.ANALYZER_PORTABLE_EXE_NAME):
        os.remove(constants.ANALYZER_PORTABLE_EXE_NAME)
    if os.path.exists(constants.HTML_REPORT_NAME):
        os.remove(constants.HTML_REPORT_NAME)
  
    delete_thumbs_folders()
    delete_reports()
    
    # for item in Path('.').iterdir():
    #     if item.is_dir():
    #         path = item / "sinf_thumbs"
    #         if path.exists():
    #             shutil.rmtree(path)
    #         path = item / "html_files"
    #         if path.exists():
    #             shutil.rmtree(path)
    #     path = item / constants.HTML_REPORT_NAME
    #     if path.exists():
    #         path.unlink()


def get_parser(device, parsers):
    filename = None
    parser_name = None
    questions = [
        {
            'type': 'list',
            'message': f'Fonte de dados (objeto: {device.name}): ',
            'name': 'source',
            'pageSize': 3,
            'choices': parsers.parsers_dict.keys()
        }
    ]
    res = prompt(questions, style=style)['source']
    if res == 'XML do PA':
        files = [entry for entry in os.listdir(
            device.folder) if entry.endswith(".xml")]
        n = len(files)
        if n == 1:
            filename = files[0]
        if n > 1:
            filename = get_file(files)['file']
        parser = parsers.parsers_dict[res](filename)
    else:
        parser = parsers.parsers_dict[res]()
    parser.set_device(device)
    return parser


def get_devices_read(devices):
    choices = [{'name': device.name, 'checked': True} for device in devices]
    questions = [
        {
            'type': 'checkbox',
            'qmark': '😃',
            'message': 'De quais objetos deseja ler os dados?',
            'name': 'options',
            'choices': choices
        }
    ]
    res = prompt(questions, style=style)['options']
    return [device for device in devices if device.name in res]


# def get_databases_delete(databases):
#     choices = []
#     for db in databases:
#         path = Path(db[1]) / ".report/config/database_name.txt"
#         checked = False if path.exists() else True
#         choices.append({
#             'name': f"Nome: {db[0]}   Pasta: {db[1]}",
#             'checked': checked,
#             'value': db[0]
#         })
#     print(choices)
#     questions = [
#         {
#             'type': 'checkbox',
#             'qmark': '😃',
#             'message': 'Quais bancos deletar?',
#             'name': 'options',
#             'choices': choices
#         }
#     ]
#     res = prompt(questions, style=style)['options']
#     return res


def get_devices_process(devices):
    choices = [{'name': device.name, 'checked': True} for device in devices]
    questions = [
        {
            'type': 'checkbox',
            'qmark': '😃',
            'message': 'Processar dados de quais objetos?',
            'name': 'options',
            'choices': choices
        }
    ]
    res = prompt(questions, style=style)['options']
    return [device for device in devices if device.name in res]


def get_file(files):
    questions = [
        {
            'type': 'list',
            'message': 'Escolha um arquivo: ',
            'name': 'file',
            'pageSize': 3,
            'choices': files
        }
    ]
    return prompt(questions, style=style)

def open_report_config():
    Popen(r's-np .report\config\report_config.yaml')

def open_analyzer_or_render_answer():
    options = {
        'Abrir analisador': 'open_analyzer',
        'Gerar relatório': 'render',
        'Finalizar': 'finish'
    }
    questions = [
        {
            'type': 'list',
            'message': 'O que deseja fazer',
            'name': 'option',
            'pageSize': 3,
            'choices': options.keys()
        }
    ]
    return options[prompt(questions, style=style)['option']]


def get_avaiable_port():
    port = 5000
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            port += 1
            continue
        return port


def inc_read_time():
    current = int(get_config('read_time'))
    current += 1
    set_config('read_time', str(current))
    return current


def set_working_dir_notebooks():
    for file in os.listdir(".report\\notebooks"):
        if file.endswith(".ipynb"):
            with codecs.open(f".report\\notebooks\\{file}", "r", "utf-8") as template:
                text = template.read()

            res = Template(text).substitute(
                cwd=os.getcwd().replace('\\', '\\\\'))
            with codecs.open(f".report\\notebooks\\{file}", "w", "utf-8") as f:
                f.write(res)


def set_working_dir_scripts():
    for file in os.listdir(".report\\scripts"):
        if file.endswith(".py"):
            with codecs.open(f".report\\scripts\\{file}", "r", "utf-8") as template:
                text = template.read()

            res = Template(text).substitute(
                cwd=os.getcwd().replace('\\', '\\\\'))
            with codecs.open(f".report\\scripts\\{file}", "w", "utf-8") as f:
                f.write(res)


def get_n_works(n_process):
    print(f"DEBUG: {n_process}")
    n_cpus = multiprocessing.cpu_count()
    n_workers = n_cpus if n_process >= n_cpus else n_process
    max_workers = config_manager.data['max_process_workers']
    if max_workers < n_workers:
        n_workers = max_workers
    return n_workers


def check_folder_structure():
    def correct_file(name):
        return True if name in [constants.ANALYZER_EXE_NAME, constants.ANALYZER_PORTABLE_EXE_NAME, constants.HTML_REPORT_NAME] else False
    n_sources = 0
    n_devices = 0
    errors = []
    files_in_folders = False
    for entry in settings.work_dir.iterdir():
        if entry.name in settings.disregard_folders:
            continue
        n_devices += 1
        if entry.is_file() and not correct_file(entry.name):
            files_in_folders = True
        elif entry.is_dir():
            for sub in entry.iterdir():
                if sub.name in settings.disregard_folders:
                    continue
                n_sources += 1
                if sub.is_file() and not correct_file(sub.name):
                    files_in_folders = True
    if files_in_folders:
        errors.append("Há arquivos soltos dentro das pastas root, pastas dos objetos ou pastas das fontes de dados, o que não corresponde a estrutura esperada.")
    if n_devices > 10:
        errors.append(f"Foi encontrado um número {n_devices} de objetos. É um número muito alto. É isso mesmo?")
    if n_sources > 15:
        errors.append(f"Foi encontrado um número {n_sources} de fontes de dados. É um número muito alto. É isso mesmo?")
    return errors

def clear_read_source(read_source):
    print(f"Deletando itens pre existentes de {read_source.folder}")
    classes =[Sms, Call, Contact, Message, Chat]
    for class_ in classes:
        items = db_session.query(class_).filter(class_.read_source == read_source).all()
        for item in items:
            db_session.delete(item)

    print(f"Deletando entrada de arquivos e thumbnails pre existentes de {read_source.folder}")
    path = Path(read_source.folder) / "sinf_thumbs"
    if path.exists():
        shutil.rmtree(path)
    db_session.query(File).filter(File.read_source == read_source).delete()
    # for item in items:
    #     db_session.delete(item)
    
    db_session.commit()    

   

if __name__ == "__main__":
    pass
