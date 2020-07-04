from flask_apscheduler import APScheduler
from sinf.servers.models import *
from sinf.servers.database import db_connect
from sinf.servers.config import output_folder
from datetime import datetime, timedelta
from sinf.servers.logger import logging
import shutil
from sqlalchemy import or_
from sinf.servers.process_manager import ProcessManager
import config as config_
from sinf.servers.com import check_telegram_broken


scheduler = APScheduler()

def delete_output_files():
    engine, db_session = db_connect()
    try:
        print("Deletando arquivos de console antigos")
        for entry in output_folder.iterdir():
            n = db_session.query(Process).filter(or_(Process.stdout == str(entry.absolute()), Process.stderr == str(entry.absolute()))).count()
            if n == 0:
                try:
                    entry.unlink()
                except PermissionError:
                    pass
    finally:
        engine.dispose()

def delete_old_processes():
    print("Checando processo antigo")
    engine, db_session = db_connect()
    try:
        limit_date = datetime.now() - timedelta(days=7)
        procs = db_session.query(Process).filter(Process.finish < limit_date).all()
        for proc in procs:
            script = Path(proc.script)
            try:
                stem = script.stem
                path = config_.recycle_bin / f"{stem}{script.suffix}"
                i = 1
                while path.exists():
                    path = config_.recycle_bin / f"{stem}_{i}{script.suffix}"
                    i += 1
                shutil.move(script, path)
                scriptmsg = str(path)
            except FileNotFoundError:
                scriptmsg = "Não existente"
            msg = f"Processo deletado: Perito: {proc.perito}, Tipo: {proc.type}, Status: {proc.status}, Script: {scriptmsg}"
            db_session.delete(proc)
            logging.warning(msg)
        db_session.commit()
    except Exception as e:
        print(e)
    finally:
        engine.dispose()

def check_processes():
    engine, db_session = db_connect()
    try:
        print("Checando processo")
        pm = ProcessManager(db_session)
        pm.check_process()
    finally:
        engine.dispose()


def update_telegram_broken():
    print("Atualizando telegram broken")
    check_telegram_broken()


class SchedulerConfig(object):
    JOBS = [
        {
            'id': 'delete_output_files',
            'func': delete_output_files,
            'trigger': 'interval',
            'minutes': 120
        },
        {
            'id': 'delete_old_processes',
            'func': delete_old_processes,
            'trigger': 'interval',
            'minutes': 120
        },
        {
            'id': 'check_process',
            'func': check_processes,
            'trigger': 'interval',
            'seconds': 30
        },
        {
            'id': 'update_telegram_broken',
            'func': update_telegram_broken,
            'trigger': 'interval',
            'minutes': 1
        }
    ]













