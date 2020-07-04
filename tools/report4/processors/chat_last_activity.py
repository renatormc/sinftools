from models import *
from database import db_session


class ChatLastActivity:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print("Gerando última mensagem do chat")
        chats = db_session.query(Chat).filter(Chat.read_source == self.read_source).all()
        for chat in chats:
            message = db_session.query(Message).filter(Message.timestamp != None, Message.chat == chat).order_by(
                Message.timestamp.desc()).first()
            if message:
                chat.last_activity = message.timestamp
                db_session.add(chat)
        db_session.commit()
