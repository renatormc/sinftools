import click
import helpers_cmd as hp
from config_manager import config_manager
import os
import sys
import shutil
import settings
import parsers
# from processor import Processor
from processors import processor_factory, get_list_processors
from models import *
import models
from database import db_session
from database import db_connect
from helpers import get_items_available

from report_maker import ReportMaker
from sinf.exe_finder import open_in_browser
from subprocess import Popen
from PyInquirer import style_from_dict, Token, prompt, Separator
from processors.proprietary_finder import ProprietaryFinder
# import multiprocessing
from time import sleep
from datetime import datetime
import importlib
import helpers_dblocal as hp_db
# from multiprocessing import Pool, cpu_count
import multiprocessing
from contextlib import contextmanager
from multiprocessing import Pool
import constants
from termcolor import cprint
import colorama
import getpass
import tempfile

colorama.init()


@contextmanager
def poolcontext(*args, **kwargs):
    pool = multiprocessing.Pool(*args, **kwargs)
    yield pool
    pool.terminate()


def process_avatars():
    read_sources = db_session.query(ReadSource).all()
    for read_source in read_sources:
        p = processor_factory('ProcessAvatars', read_source)
        p.run()


@click.group()
# @click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx):
    pass
    # ctx.obj['DEBUG'] = debug


@cli.command()
@click.option('--grouped/--no-grouped', default=False)
@click.option('--dbtype', type=click.Choice(['sqlite', 'mysql', 'postgres']), default='sqlite')
def init(grouped, dbtype):
   
      
    # hp.askfor_update()
    if os.path.exists(".report"):
        hp.instruct_continue(
            "Já existe um projeto em andamento nessa pasta. Deseja reiniciá-lo? Isso implicará a perda de tudo que foi feito até agora.")
    errors = hp.check_folder_structure()
    if errors:
        print("\nSua estrutura de pastas parece não atender aos critérios necessários. Leia o tutorial no SINFWeb.")
        print("\nPossíveis erros encontrados: ")
        # print("\nPossíveis erros encontrados:")
        for error in errors:
            cprint(f" -> {error}", "yellow")
            # print(error)
        print("\n")
        hp.show_options_cancel("O que deseja fazer?", [
                               'Continuar mesmo assim. Os erros detectados são falsos.'], cancel_option=True)
        # hp.instruct_continue("")

    hp.reset(dbtype=dbtype)
    sleep(1)
    os.mkdir('.report')
    os.system("attrib +h " + ".report")
    shutil.copytree(settings.app_dir / "scripts", ".report/scripts")
    hp.set_working_dir_scripts()
    # shutil.copytree(settings.app_dir / "notebooks", ".report/notebooks")
    shutil.copy(settings.app_dir / "reader/static/image/desconhecido.png",
                ".report/desconhecido.png")
    # hp.set_working_dir_notebooks()
    shutil.copytree(settings.app_dir / "config_files/config",
                    Path(".report/config"))
    config_manager.set_grouped(grouped)

    from database import init_db
    print(f"Gerando banco de dados {dbtype}")
    if dbtype != 'sqlite':
        hp_db.create_database_localdb(type=dbtype)
        hp_db.drop_orphan_databases(
            type=dbtype, exclude=[config_manager.database_name])
        n_cpu = multiprocessing.cpu_count()
        config_manager.data['n_workers'] = n_cpu if n_cpu <= 8 else 8
        config_manager.save()

    config_manager.load_database_name()
    db_connect()
    importlib.reload(models)
    init_db()
    hp.copy_config_files(overwrite=True)
    # shutil.copy(settings.app_dir / "go/starter_normal.exe",
    #             constants.ANALYZER_EXE_NAME)
    shutil.copy(settings.app_dir / constants.ANALYZER_EXE_NAME,
                constants.ANALYZER_EXE_NAME)
    print("\nAmbiente preparado. Antes de processar não se esqueça de editar os arquivos \"config_source.yaml\" que se encontram dentro de cada pasta de fonte de dados.")


# def process_worker(processes):
#     read_source_id, parser = processes
#     read_source = db_session.query(ReadSource).get(read_source_id)
#     print(f"Iniciando processamento {read_source.folder}")
#     hp.clear_read_source(read_source)
#     parser.run()
#     parser = None
#     for item in config_manager.data['processors']:
#         processor = processor_factory(item, read_source)
#         processor.run()
#     config_manager.set_process(read_source.folder, False)
#     read_source.process = False
#     db_session.add(read_source)
#     db_session.commit()

# def process_worker(read_source_id):
#     path = settings.app_dir / "process.py"
#     os.system(f"s-py \"{path}\" {read_source_id}")


@cli.command()
def process():
    start_time = datetime.now()

    # atualizar arquivos yaml
    hp.update_sources()
    read_sources = db_session.query(ReadSource).filter(
        ReadSource.process == True).all()
    # for read_source in read_sources:
    #     if read_source.source_type == 'xml_ufed':
    #         config_manager.set_data_file(read_source.folder)

    hp.update_sources()
    read_sources = db_session.query(ReadSource).filter(
        ReadSource.process == True).all()
    for read_source in read_sources:
        print(f"Iniciando processamento {read_source.folder}")
        parser = parsers.parsers_dict[read_source.source_type]()
        parser.set_read_source(read_source)
        msgs = parser.check_env()
        if msgs:
            for msg in msgs:
                print(msg)
            sys.exit()
        hp.clear_read_source(read_source)
        parser.run()
        del parser
        for item in config_manager.data['processors']:
            processor = processor_factory(item, read_source)
            processor.run()
        config_manager.set_process(read_source.folder, False)
        read_source.process = False
        db_session.add(read_source)
        db_session.commit()
    # for process in processes:
    #     read_source, parser = process

    #     hp.clear_read_source(read_source)
    #     parser.run()
    #     parser = None
    #     for item in config_manager.data['processors']:
    #         processor = processor_factory(item, read_source)
    #         processor.run()
    #     config_manager.set_process(read_source.folder, False)
    #     read_source.process = False
    #     db_session.add(read_source)
    #     db_session.commit()
    delta = datetime.now() - start_time
    print(f"\nProcessamento finalizado. Tempo gasto: {delta}")


@cli.command()
def render():
    op = hp.show_options_cancel("Configurações do relatório:", options=[
                                'Utilizar configurações padrão', 'Editar arquivo de configurações antes de continuar'])
    if op == 'Editar arquivo de configurações antes de continuar':
        hp.open_report_config()
        hp.instruct_continue("")
        config_manager.load_report_config()
    hp.delete_reports()
    if config_manager.report_config['folder'] == 'device':
        devices = db_session.query(Device).all()
        for device in devices:
            report_maker = ReportMaker()
            report_maker.set_item_source(device)
            report_maker.generate_html_files()
    if config_manager.report_config['folder'] == 'read_source':
        read_sources = db_session.query(ReadSource).all()
        for rs in read_sources:
            report_maker = ReportMaker()
            report_maker.set_item_source(rs)
            report_maker.generate_html_files()


@cli.command()
def update():
    hp.copy_config_files()
    hp.update_sources()
    process_avatars()


@cli.command()
def delete_unchecked():
    p = processor_factory("DeleteUnchecked")
    p.run()


@cli.command()
def portable():
    print(
        f"Migrando banco de dados de {config_manager.database_type} para sqlite.")
    path = Path(".report/db.db")
    if path.exists():
        path.unlink()
    from local2sqlite.migrate import run_migrate
    run_migrate()

# @cli.command()
# def portable():
#     if os.path.exists(".report\\gui_server"):
#         shutil.rmtree(".report\\gui_server")
#     hp.copy_folder(settings.app_dir / "reader/dist/gui_server",
#                    ".report\\gui_server")
#     shutil.copy(settings.app_dir / "go/starter_portable.exe",
#                 constants.ANALYZER_PORTABLE_EXE_NAME)
#     if config_manager.is_localdb():
#         print(
#             f"Migrando banco de dados de {config_manager.database_type} para sqlite.")
#         path = Path(".report/db.db")
#         if path.exists():
#             path.unlink()
#         from local2sqlite.migrate import run_migrate
#         run_migrate()


# @cli.command()
# def dbb():
#     os.system("s-dbb .report\\db.db")


@cli.command()
def db_config():
    path = Path(f"{settings.sinftools_dir}/var/config/sinf_report_db.json")
    if not path.exists():
        if not path.exists():
            shutil.copy(
                Path(settings.app_dir / "dev/sinf_report_db.json"), path)
    mariadb_folder = Path(r'C:\Program Files\MariaDB 10.4\bin')
    while not mariadb_folder.exists():
        folder = input(
            "Entre a pasta de instalação do MariaDB: (ex: \"C:\Program Files\MariaDB 10.4\bin\"):")
        mariadb_folder = Path(folder)
    user = input("Usuário root do MariaDB: ")
    # password = getpass.getpass(prompt='Senha: ')
    try:
        sql = """CREATE USER IF NOT EXISTS 'sinf'@'localhost' IDENTIFIED BY 'sptcICLR.';\nGRANT ALL PRIVILEGES ON *.* TO 'sinf'@'localhost';
        """
        with tempfile.NamedTemporaryFile(suffix=".sql", mode="w", delete=False) as f:
            f.write(sql)
        cmd = f'("{mariadb_folder}\\mysql" -u {user} -p < "{f.name}")'
        os.system(cmd)
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data['user'] = 'sinf'
        data['password'] = 'sptcICLR.'
        data['mysql_bin_folder'] = str(mariadb_folder)
        with path.open("w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
        print("Banco de dados configurado com sucesso.")
    except Exception as e:
        print(e)


@cli.command()
def list_dbs():
    dbs = hp_db.get_db_list()
    type_ = config_manager.database_type
    for db in dbs:
        print("-----------------------------------------")
        print(f"NOME: {db[0]}\nPASTA: {db[1]}\nTIPO: {type_}")


@cli.command()
@click.option('--dbtype', type=click.Choice(['mysql', 'postgres']), default='postgres')
def dropdb(dbtype):
    hp_db.drop_orphan_databases(type=dbtype)


@cli.command()
@click.option('--edit/--no-edit', default=False)
@click.option('--search', default="")
@click.option('--new')
def script(edit, search, new):
    scripts = os.listdir(".report\\scripts")
    if new:
        new_script = f".report\\scripts\\{new}.py"
        shutil.copy(".report\\scripts\\exemplo.py", new_script)
        Popen(f"\"{settings.sinftools_dir}\\extras\\Python\\pythonw.exe\" \"{settings.sinftools_dir}\\extras\\Python\\Scripts\\idlex.pyw\" \"{new_script}\"")
        return
    if search != "":
        scripts = list(filter(lambda x: search in x, scripts))

    if scripts:
        questions = [
            {
                'type': 'list',
                'message': "Selecione o script",
                'name': 'script',
                'pageSize': 3,
                'choices': scripts
            }
        ]
        script = prompt(questions, style=hp.style)['script']
        if edit:
            Popen(
                f"\"{settings.sinftools_dir}\\extras\\Python\\pythonw.exe\" \"{settings.sinftools_dir}\\extras\\Python\\Scripts\\idlex.pyw\" .report\\scripts\\{script}")
        else:
            os.system(
                f"\"{settings.sinftools_dir}\\extras\\Python\\python.exe\" .report\\scripts\\{script}")
    else:
        print("Nenhum script com este nome foi encontrado")


# @cli.command()
# def avatar():
#     for rs in db_session.query(ReadSource).distinct(ReadSource.folder):
#         folder = os.path.abspath(rs.folder)
#         object = Path(rs.folder).parent.name
#         print(
#             f"\nOBJETO {object} **************************************************")
#         print("Para Android: ")
#         cmd = f"execfile(r'{settings.sinftools_dir}\\tools\\ufed\\ufed.py');ufed.exportar_avatars(r'{folder}')"
#         print(cmd)
#         print("\nPara Iphone: ")
#         cmd = f"execfile(r'{settings.sinftools_dir}\\tools\\ufed\\ufed.py');ufed.exportar_avatars_iphone(r'{folder}')"
#         print(cmd)


@cli.command()
@click.option('--mode', default="waitress")
def analyzer(mode):
    os.environ['exec_mode'] = mode
    path = settings.reader_folder / "server.py"
    python = settings.sinftools_dir / "extras/Python/python.exe"
    Popen(f'"{python}" "{path}" {mode}')


@cli.command()
@click.option('--processors', default="list")
def extra_process(processors):
    if processors == 'list':
        print("Utilize s-report extra_process --processors Processor1,Processor2,...\n")
        for p in get_list_processors():
            print(p)
    else:
        start_time = datetime.now()
        processors = processors.split(",")
        read_sources = db_session.query(ReadSource).all()
        for p in processors:
            for rs in read_sources:
                processor = processor_factory(p, rs)
                processor.run()
        delta = datetime.now() - start_time
        print(f"Processamento finalizado. Tempo gasto: {delta}")


@cli.command()
@click.option('--tags', required=True)
@click.option('--item', type=click.Choice(['image', 'video', 'chat']), required=True)
@click.option('--n_cols', type=int, default=3)
@click.option('--caption', default="Exemplo de mensagens de bate-papo")
def word(tags, item, n_cols, caption):
    from word_handler import WordHandler
    tags = [item.strip() for item in tags.split(",")]
    for tag in tags:
        if not db_session.query(Tag).filter_by(name=tag).count():
            print(f'Tag "{tag}" não existe.')
            return
    wh = WordHandler()
    if item == 'image':
        files = db_session.query(File).filter(
            File.type_ == 'image', File.tags.any(Tag.name.in_(tags))).all()

        if not files:
            print(f"Nenhuma imagem marcada com as tags {tags}")
            return
        files = [file_.path for file_ in files]
        wh.insert_images(n_cols, files)
    elif item == 'video':
        files = db_session.query(File).filter(
            File.type_ == 'video', File.tags.any(Tag.name.in_(tags))).all()
        if not files:
            print(f"Nenhum video marcado com as tags {tags}")
            return
        files = [file_.thumb_path for file_ in files]
        wh.insert_images(n_cols, files)
    elif item == 'chat':
        messages = db_session.query(Message).filter(
            Message.tags.any(Tag.name.in_(tags))).all()
        wh.insert_chat_messages_table(caption, messages)


@cli.command()
def mark_all_to_process():
    for rs in db_session.query(ReadSource).all():
        print(rs.folder)
        config_manager.set_process(rs.folder, True)


@cli.command()
def gen_yaml():
    p = Path('config_source.yaml')
    if not p.exists():
        shutil.copy(settings.app_dir /
                    "config_files/config_source.yaml", p)


@cli.command()
def db_name():
    database_name = config_manager.database_name
    if database_name:
        print(database_name)


if __name__ == '__main__':
    cli(obj={})
