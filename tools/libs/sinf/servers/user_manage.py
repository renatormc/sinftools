import win32net
from datetime import datetime, timedelta
import os
from sinf.servers.models import *
from sinf.servers.database import db_session
import subprocess
from sinf.servers import config as cf


def get_connection_type():
    cmd = f"query session |findstr Ativo"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    text = output.decode("utf-8")
    if "Ativo" in text:
        return 'rdp' if 'rdp' in text else 'local'


def get_last_logon_time(username=None):
    username = cf.config_local['shared_user']
    # if not username:
    #     username = os.getlogin()
    users, nusers, _ = win32net.NetUserEnum(None, 2)

    for user in users:
        try:
            if user['name'] == username:
                return datetime.fromtimestamp(user['last_logon'])
        except OSError:
            return


def compare_timestamp(t1, t2):
    return abs(t2-t1) < timedelta(seconds=30)


def who_is_connected():
    type_connection = get_connection_type()

    # Ningúem está conectado
    if not type_connection:
        return

    # Se a última pessoa que declarou intenção de conectar foi em um horário muito próximo do horário do último logon
    # então foi ela mesma que conectou
    last_logon = get_last_logon_time()
    doc = db_session.query(Document).filter_by(key="who_want_connect").first()
    if doc and last_logon:
        aux = datetime.strptime(doc.value['timestamp'], "%d/%m/%Y %H:%M:%S")
        data = {
            'name': doc.value['name'],
            'timestamp': datetime.strptime(doc.value['timestamp'], "%d/%m/%Y %H:%M:%S"),
            'type_connection': type_connection
        }
        if compare_timestamp(data['timestamp'], last_logon):
            return data

    # Se não há registro de intenção de algúem conectar ou se o horário que informou
    # é muito diferente do horário da última conexão
    # então não é possível afirmar quem é que de fato está conectado
    return {
        'name': 'Alguém',
        'timestamp': last_logon,
        'type_connection': type_connection
    }


def post_connect_intent(name, timestamp=None):
    timestamp = timestamp or datetime.now()
    doc = db_session.query(Document).filter_by(key="who_want_connect").first()
    if not doc:
        doc = Document()
        doc.key = "who_want_connect"
    doc.value = {
        "name": name,
        "timestamp": timestamp.strftime("%d/%m/%Y %H:%M:%S")
    }
    db_session.add(doc)
    db_session.commit()
