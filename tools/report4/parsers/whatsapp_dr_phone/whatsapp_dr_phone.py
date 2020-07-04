from parsers.parser_base import ParserBase
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
from models import *
from database import db_session
from helpers_cmd import progress
import os
import parsers.whatsapp_dr_phone.helpers as hp
import pandas as pd


class WhatsAppDrPhone(ParserBase):
    def __init__(self):
        self.fields = ['chat', 'body', 'timestamp', 'from']
        self.start_line = 10
        self.df = None
        self.lines = None

    def check_env(self):
        self.path_html = Path(self.read_source.folder) / "HTML/WhatsApp.html"
        msgs = []
        if not self.path_html.exists():
            msgs.append(
                f'Não foi encontrada o arquivo HTML/WhatsApp.html')
        return msgs


    def new_message(self):
        return {field: "" for field in self.fields}

    def load_df(self):
        html_doc = self.path_html.read_text(encoding="utf-8")
        self.lines = html_doc.split("\n")
        messages = []

        message = None
        current_chat = ""
        for line in self.lines[self.start_line:]:
        #     message = new_message()
            type_, value = hp.parse_line(line)
        
            if type_ == "chat_identifier":
                current_chat = value
            elif type_ == "timestamp":
                if message is not None:
                    messages.append(message)
                message = self.new_message()
                message['chat'] = current_chat
                message['timestamp'] = value
            elif type_ == "body":
                owner, text = value
                if owner:
                    message['from'] = 'proprietário'
                message['body'] = text
            elif type_ == "from":
                message['from'] = value            
        self.df = pd.DataFrame(messages)

    def ajust_df(self):
        self.df.timestamp = pd.to_datetime(self.df.timestamp)
        self.df = self.df.sort_values(by=['chat', 'timestamp'], ascending=[True, True])

    def add_participant(self, identifier, name):
        name = name or identifier or "Desconhecido"
        identifier = identifier or name or "Desconhecido"
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
       
        name = name or identifier or "Desconhecido"
        identifier = identifier or name or "Desconhecido"
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
        print("Iniciando parsing do HTML")
        self.load_df()
        self.ajust_df()
        for c in self.df.chat.unique():
            print(f"Efetuando parsing do chat {c}")
            df2 = self.df[self.df.chat == c]
            chat = self.add_chat(c, c)
            
            for i, item in df2.iterrows():
                message = Message()
                from_id = item['from'].replace("@g.us", "").replace("@s.whatsapp.net", "")
                message.from_ = self.add_participant(from_id, from_id)
                if not message.from_ in chat.participants:
                    chat.participants.append(message.from_)
                message.body = item['body']
                message.timestamp = item['timestamp']
                message.chat = chat
                self.add(message)
            self.add(chat)
            self.commit()

        