from parsers.parser_base import ParserBase
import sqlalchemy as sa
from sqlalchemy import select, distinct
from pathlib import Path
from models import *
from database import db_session
from database import db_session
from datetime import datetime
from helpers_cmd import progress
import json

class FBMessenger2Db2(ParserBase):
    def __init__(self):
        pass

    def check_env(self):
        msgs = []
        self.path_db = Path(self.read_source.folder) / 'threads_db2'
        if not self.path_db.exists():
            msgs.append(f"Não foi encontrado o arquivo {self.path_db}")
        return msgs

    def __read_database(self):
        url = f"sqlite:///{self.path_db}"
        self.engine = sa.create_engine(url)
        self.conn = self.engine.connect()
        self.meta = sa.MetaData()
        self.meta.reflect(bind=self.engine)
        self.table_threads = self.meta.tables['threads']
        self.table_messages = self.meta.tables['messages']

        self.cols = [
            self.table_messages.c.timestamp_ms,
            self.table_messages.c.text,
            self.table_messages.c.sender,
            self.table_threads.c.thread_key
        ]

    def add_participant(self, identifier, name):
        if not identifier and not name:
            return None
        participant = db_session.query(Participant).filter(
            Participant.identifier == identifier, Participant.name == name).first()
        if not participant:
            participant = Participant()
            participant.identifier = identifier
            participant.name = name
            participant.read_source = self.read_source
            self.add(participant)
            self.commit()
        return participant

    def add_chat(self, identifier, name):
        if not identifier and not name:
            return None
        chat = db_session.query(Chat).filter(
            Chat.identifier == identifier, Chat.name == name).first()
        if not chat:
            chat = Chat()
            chat.identifier = identifier
            chat.name = name
            chat.read_source = self.read_source
            chat.source = self.read_source.chat_source
            self.add(chat)
            self.commit()
        return chat

    def run(self):
        self.__read_database()
        stm = self.table_messages.select().order_by(sa.asc(self.table_messages.c.thread_key), sa.asc(self.table_messages.c.timestamp_ms))
        res_messages = self.conn.execute(stm).fetchall()

        m = res_messages[0]
        chat = self.add_chat(m['thread_key'], m['thread_key'])
        current_thread_key = m['thread_key']
        n = len(res_messages)
        for i, m in enumerate(res_messages):
            progress(i, n)
            if current_thread_key != m['thread_key']:
                db_session.add(chat)
                chat = self.add_chat(m['thread_key'], m['thread_key'])
                current_thread_key = m['thread_key']
            message = Message()
            sender = json.loads(m['sender']) if m['sender'] is not None else None
            message.extra = json.loads(m['attachments']) if m['attachments'] is not None else None
            if sender:
                message.from_ = self.add_participant(sender['user_key'], sender['name'])
                if not message.from_ in chat.participants:
                    chat.participants.append(message.from_)
            try:
                timestamp = datetime.fromtimestamp(
                    int(m['timestamp_ms'])/1000)
            except:
                timestamp = None
            message.timestamp = timestamp
            message.read_source = self.read_source
            message.chat_id = chat.id
            message.body = m['text']
            db_session.add(message)
        db_session.commit()
