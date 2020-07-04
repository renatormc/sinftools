from parsers.parser_base import ParserBase
import sqlalchemy as sa
from sqlalchemy import select, distinct
from pathlib import Path
from models import *
from database import db_session
from database import db_session
from datetime import datetime
from helpers_cmd import progress


class FBMessenger2Db(ParserBase):
    def __init__(self):
        pass

    def check_env(self):
        msgs = []
        self.path_core = Path(self.read_source.folder) / 'core.db'
        if not self.path_core.exists():
            msgs.append(f"Não foi encontrado o arquivo {self.path_core}")
        return msgs

    def __read_database(self):
        url = f"sqlite:///{self.path_core}"
        self.engine = sa.create_engine(url)
        self.conn = self.engine.connect()
        self.meta = sa.MetaData()
        self.meta.reflect(bind=self.engine)
        self.table_threads = self.meta.tables['threads']
        self.table_messages = self.meta.tables['messages']

        self.cols = [
            self.table_messages.c.timestamp,
            self.table_messages.c.snippet,
            self.table_messages.c.attachment_filename,
            self.table_messages.c.user_id,
            self.table_messages.c.sender,
            self.table_threads.c.thread_key,
            self.table_threads.c.thread_name,
            self.table_threads.c.updated_timestamp
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
            self.add(chat)
            self.commit()
        return chat

    def run(self):
        self.__read_database()
        stm = select(self.cols).select_from(sa.join(self.table_messages,
                                                    self.table_threads, self.table_messages.c.thread_key == self.table_threads.c.thread_key, isouter=True)).order_by(sa.asc(self.table_messages.c.thread_key), sa.asc(self.table_messages.c.timestamp))
        res_messages = self.conn.execute(stm).fetchall()

        m = res_messages[0]
        chat = self.add_chat(m['thread_key'], m['thread_name'])
        current_thread_key = m['thread_key']
        n = len(res_messages)
        for i, m in enumerate(res_messages):
            progress(i, n)
            if current_thread_key != m['thread_key']:
                db_session.add(chat)
                chat = self.add_chat(m['thread_key'], m['thread_name'])
                current_thread_key = m['thread_key']
            message = Message()
            message.from_ = self.add_participant(m['user_id'], m['sender'])
            if not message.from_ in chat.participants:
                chat.participants.append(message.from_)
            try:
                timestamp = datetime.fromtimestamp(
                    int(m['timestamp'])/1000)
            except:
                timestamp = None
            message.timestamp = timestamp
            message.read_source = self.read_source
            message.chat_id = chat.id
            message.body = m['snippet']
            db_session.add(message)
        db_session.commit()
