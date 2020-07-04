from flask import Blueprint, jsonify, request
from schemas import *
from models import *
from database import db_session
import subprocess
from helpers import get_connected, set_connected

api = Blueprint('api', __name__)


@api.route("/processes")
def processes():
    processes = db_session.query(Process).order_by(
        Process.queue_order.asc(), Process.start_waiting.asc()).all()
    schema = ProcessSchema(many=True)
    return jsonify(schema.dump(processes).data)


@api.route("/process/<int:id>")
def process(id):
    process = db_session.query(Process).get(id)
    schema = ProcessSchema()
    return jsonify(schema.dump(process).data)


@api.route("/someone-connected")
def someone_connected():
    cmd = f"query session |findstr Ativo"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    text = output.decode("utf-8")
    if "Ativo" in text:
        doc = get_connected()
        if "rdp" in text:
            msg =  f"{doc['name']} está conectado desde {doc['timestamp']} de forma remota."
        else:
            msg = f"{doc['name']} está conectado desde {doc['timestamp']} de forma local, não remota."
        return msg
    return "no"


@api.route("/who-connected", methods=('POST',))
def who_connected_post():
    data = request.get_json()
    set_connected(data['name'])
    return data['name']


