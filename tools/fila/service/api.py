from flask import Blueprint, jsonify, request, abort
from schemas import *
from sinf.servers.models import *
from sinf.servers.database import db_session
import subprocess
from helpers import get_connected, set_connected
from sinf.servers.telegram_api import send_message, UserNotRegistered
from sinf.servers.updater import Updater
from sinf.servers.process_manager import ProcessManager
import sinf.servers.repo as repo
from sinf.servers.markers import get_scannable_drives
import psutil
from auth import jwt_required, get_user_claims
from sinf.servers import user_manage


api = Blueprint('api', __name__)


@api.route("/update-sinftools")
@jwt_required
def update_sinftools():
    """Atualiza o sinftools com os dados do servidor do sinfweb"""
    updater = Updater()
    return updater.update()


@api.route("/processes")
@jwt_required
def processes():
    processes = db_session.query(Process).order_by(
        Process.start_waiting.asc()).all()
    schema = ProcessSchema(many=True)
    return jsonify(schema.dump(processes).data)


@api.route("/check-process")
@jwt_required
def check_process():
    print("Checando por solicitação remota")
    pm = ProcessManager(db_session)
    pm.check_process()
    return "ok"


@api.route("/process/<int:id>")
@jwt_required
def process_script(id):
    process = db_session.query(Process).get(id)
    schema = ProcessSchema()
    return jsonify(schema.dump(process).data)


@api.route("/process-console/<int:id>")
@jwt_required
def process_console(id):
    """Recebe o id do processo e retorna o texto do console do processo"""
    process = db_session.query(Process).get(id)
    stdout = process.get_output_tail().replace("\n\r", "<br>").replace(
        "\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")
    stderr = process.get_output_tail(stderr=True).replace("\n\r", "<br>").replace(
        "\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")
    return jsonify({"stdout": stdout, "stderr": stderr})


@api.route("/send-telegram", methods=("POST",))
def send_telegram():
    """Recebe o nome do usuário e o texto da mensagem e faz o envio para o celular do usuário"""
    data = request.get_json()
    try:
        send_message(data['username'], data['text'])
    except UserNotRegistered:
        return abort(404)
    except KeyError:
        return abort(404)
    return "ok"


@api.route("/process-script/<int:id>")
@jwt_required
def process(id):
    """Recebe o id de um processo e retorna o texto o script dele"""
    process = db_session.query(Process).get(id)
    path = Path(process.script)
    text = f"Script: {path}"
    text += "<br>---------------------------------------------------------------------------------------------------------<br>"
    text += path.read_text().replace("\n", "<br>")
    return jsonify({"text": text})


@api.route("/who-is-connected")
@jwt_required
def who_is_connected():
    """Consultar ao servidor se há algum usuário logado"""
    who = user_manage.who_is_connected()
    if not who:
        return "nobody"
    timestamp = who['timestamp'].strftime(
        "%d/%m/%Y %H:%M:%S") if who['timestamp'] else ""
    message = f"{who['name']} está conectado desde {timestamp}. Tipo da conexão: {who['type_connection']}"
    return message


@api.route("/connection-intent", methods=('POST',))
@jwt_required
def post_connection_intent():
    """Pega o nome do usuário do token que ele envia no cabeçalho da requisição e salva no banco a intenção dele de se contectar via RDP
    Essa intenção será confirmada quando alguém logar via RDP. Outro script ficará programado para ser executado toda vez que alguém fizer logon"""
    data = get_user_claims()
    user_manage.post_connect_intent(data['name'])
    return data['name']


@api.route("/set-telegram-broken-url", methods=('POST',))
def set_telegram_broken_url():
    """Quando um servidor descobre que possui conexão com a internet ele informa os demais que vai ser o broker do telegram
    Então todo mundo que quiser enviar mensagem via telegram deve enviar para ele para que ele envie para o celular do perito"""
    data = request.get_json()
    repo.set_telegram_broken_url(data['value'])
    return "ok"


@api.route("/get-disk-usage")
@jwt_required
def get_disk_usage():
    ret = []
    for item in get_scannable_drives():
        info = psutil.disk_usage(item['drive'])
        percent_used = int(info.percent)
        percent_free = 100 - percent_used
        ret.append({
            'name': item['name'],
            'letter': item['drive'][:-1],
            'total': info.total,
            'used': info.used,
            'free': info.free,
            'percent_used': percent_used,
            'percent_free': percent_free
        })
    return jsonify(ret)


@api.route("/blocking-user")
@jwt_required
def blocking_user():
    pm = ProcessManager(db_session)
    ret = {'blocked': False, 'user': None, 'timestamp': None}
    user = pm.get_blocking_user()
    if user:
        ret['blocked'] = True
        ret['user'] = user['user']
        ret['timestamp'] = user['timestamp'].strftime("%d/%m/%Y %H:%M:%S")
    return jsonify(ret)
