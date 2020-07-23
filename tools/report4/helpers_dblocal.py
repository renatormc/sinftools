import sqlalchemy as sa
from config_manager import config_manager
import subprocess
import os
from config_manager import config_manager
import settings
from pathlib import Path

def get_db_list_mysql(only_current_workdir=False):
    dbconfig = config_manager.get_db_local_config()
    engine = sa.create_engine(
        f"mysql://{dbconfig['user']}:{dbconfig['password']}@localhost")
    insp = sa.inspect(engine)
    dblist = []
    db_list = [item for item in insp.get_schema_names()
               if item.startswith("sinf_report")]
    for db in db_list:
        engine = sa.create_engine(
            f"mysql://{dbconfig['user']}:{dbconfig['password']}@localhost/{db}")
        with engine.connect() as con:
            try:
                sql = "select *  from config where `key` = 'workdir'"
                rs = con.execute(sql)
                res = rs.fetchone()
                if not res:
                    raise Exception("Error")
                if not only_current_workdir or (res[1] == str(settings.work_dir)):
                    dblist.append((db, res[1]))
            except Exception as e:
                if not only_current_workdir:
                    dblist.append((db, None))
    return dblist


def get_database_info(host, dbconfig):
    user = dbconfig['user']
    os.environ['PGPASSWORD'] = dbconfig['password']
    executable = f"{dbconfig['postgres_bin_folder']}\psql" if os.name == 'nt' else 'psql'
    records, _ = subprocess.Popen([executable, '-lA',
                                   '-F\x02', '-R\x01', '-h', host, '-U', user], stdout=subprocess.PIPE).communicate()
    records = records.split(bytes.fromhex('01'))
    header = records[1].split(bytes.fromhex('02'))
    items = []
    for line in records[2:-1]:
        res = {item[0].decode('windows-1252'): item[1].decode('windows-1252')
               for item in zip(header, line.split(bytes.fromhex('02')))}
        items.append(res)
    return items


def get_db_list_postgres(only_current_workdir=False):
    dbconfig = config_manager.get_db_local_config()
    dblist = []
    db_list = []
    try:
        db_list = [item['Nome'] for item in get_database_info(
            'localhost', dbconfig) if item['Nome'].startswith("sinf_report")]
    except KeyError:
        pass
    for db in db_list:
        engine = sa.create_engine(
            f"postgresql://{dbconfig['user']}:{dbconfig['password']}@localhost/{db}")
        with engine.connect() as con:
            try:
                rs = con.execute("select * from config where key = 'workdir'")
                res = rs.fetchone()
                if not res:
                    raise Exception("Error")
                if not only_current_workdir or (res[1] == str(settings.work_dir)):
                    dblist.append((db, res[1]))

            except Exception as e:
                if not only_current_workdir:
                    dblist.append((db, None))
    return dblist


def get_db_list(only_current_workdir=False, type=None):
    type_ = type or config_manager.database_type
    if type_ == 'postgres':
        return get_db_list_postgres(only_current_workdir=only_current_workdir)
    if type_ == 'mysql':
        return get_db_list_mysql(only_current_workdir=only_current_workdir)


def drop_database(name, dbtype=None):
    dbtype = dbtype or config_manager.database_type
    dbconfig = config_manager.get_db_local_config()
    if dbtype == 'postgres':
        os.environ['PGPASSWORD'] = dbconfig['password']
        dropdb =f"{dbconfig['postgres_bin_folder']}\\dropdb\"" if os.name == 'nt' else 'dropdb'
        cmd = f"(\"{dropdb}\" -h localhost -U {dbconfig['user']} {name})"
        os.system(cmd)
    elif dbtype == 'mysql':
        mysql = f"{dbconfig['mysql_bin_folder']}\\mysql" if os.name == 'nt' else 'mysql'
        cmd = f"(\"{mysql}\" -u {dbconfig['user']} -p{dbconfig['password']} -e \"DROP DATABASE {name};\")"
        os.system(cmd)


# def drop_database_workdir(dbtype):
#     if dbtype == 'sqlite':
#         return
#     dblist = get_db_list(only_current_workdir=True)
#     if dblist:
#         for db in dblist:
#             print(f"Deletando banco {db[0]}")
#             drop_database(db[0], dbtype=dbtype)


def create_database_localdb(type="postgres"):
    dbconfig = config_manager.get_db_local_config()
    config_manager.generate_database_name(type=type)
    config_manager.load_database_name()
    from sqlalchemy_utils import create_database, database_exists
    url = config_manager.get_database_url()
    if not database_exists(url):
        if config_manager.database_type == 'mysql':
            mysql = f"{dbconfig['mysql_bin_folder']}\\mysql" if os.name == 'nt' else 'mysql'
            cmd = f"(\"{mysql}\" -u {dbconfig['user']} -p{dbconfig['password']} -e \"CREATE DATABASE {config_manager.database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\")"
            os.system(cmd)
        else:
            create_database(url)


def drop_orphan_databases(type="postgres", exclude=[]):
    databases = get_db_list(type=type)
    for db in databases:
        to_delete = True
        if db[1]:
            path = Path(db[1]) / ".report/config/database_name.txt"
            if path.exists():
                with path.open("r", encoding="utf-8") as f:
                    text = f.read()
                name = text.split("|")[1]
                if name == db[0]:
                    to_delete = False
        if to_delete and db[0] not in exclude:
            print(f'Deletando banco orfão "{db[0]}"')
            drop_database(db[0], dbtype=type)

    
if __name__ == "__main__":
    res = get_db_list_mysql(only_current_workdir=True)
    print(res)
