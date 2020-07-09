import config
import sinf_requests
from requests.exceptions import ConnectionError
from database import db_session
from models import *


class ContactNotRegistered(Exception):
    pass

def get_chat_id(name):
    user = db_session.query(User).filter(User.name.ilike(f"{name}")).first()
    if user:
        return user.telegram_chat_id

def get_contact_name(chat_id):
    user = db_session.query(User).filter(User.telegram_chat_id == chat_id).first()
    if user:
        return user.name
   

def bot_send_message(name, text):
    try:
        url = f"{config.config_local['sinfbot_url']}/send-message"
        req = sinf_requests.Requester(config.SINF_TOKEN)
        req.post(url, json={'name': name, 'text': text})
    except ConnectionError:
        return "Não foi possível se conectar ao bot"
