
from flask import Flask, request, abort, make_response, jsonify
from .sinfbot import bot
import config
from helpers.auth import jwt_required
from . import helpers
from telegram.error import BadRequest

app = Flask(__name__)

@app.route("/send-message", methods=("POST",))
@jwt_required
def send_message():
    data = request.json
    try:
        chat_id = helpers.get_chat_id(data['name'])
        bot.sendMessage(chat_id=chat_id, text=data['text'])
    except (BadRequest, helpers.ContactNotRegistered) as e:
        abort(make_response(jsonify(message=str(e)), 403))
    except KeyError:
        abort(make_response(jsonify(message="Wrong data"), 403))
    return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.local_config['port'], debug=config.local_config['debug'])