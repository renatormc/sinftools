from models import *
from database import db_session

class ChatMessageCount:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print("Contando mensagens por chat")
        chats = db_session.query(Chat).filter_by(read_source_id=self.read_source.id).all()
        for chat in chats:
            chat.n_messages = chat.messages.count()
            db_session.add(chat)
        db_session.commit()