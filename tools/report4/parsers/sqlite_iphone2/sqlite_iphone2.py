from parsers.parser_base import ParserBase
import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd
from models import *
from database import db_session
from helpers_cmd import progress
import os


def convert_timestamp(value):
    int_ = 978307200 + value
    return datetime.fromtimestamp(int_)


class SqliteIphone2(ParserBase):
    def __init__(self):
        self.unknow_chat_count = 0
        self.path_sqlite = None
        self.attachments_folder = None
        self.conn = None
        self.df_messages = None
        self.df_profile_push_name = None
        self.df_media_item = None
        self.df_chat_session = None

    def check_env(self):
        self.path_sqlite = Path(self.read_source.folder) / "ChatStorage.sqlite"
        self.attachments_folder = Path(self.read_source.folder) / "Media"
        msgs = []
        if not self.path_sqlite.exists():
            msgs.append(
                f'Não foi encontrado o arquivo ChatStorage.sqlite na pasta {self.read_source.folder}')
        if not self.attachments_folder.exists():
            msgs.append(
                f"Não foi encontrada a pasta \"{str(self.attachments_folder)}\"")
        return msgs

    def run(self):
        self.path_sqlite = Path(self.read_source.folder) / "ChatStorage.sqlite"
        self.attachments_folder = Path(self.read_source.folder) / "Media"
        self.conn = sqlite3.connect(str(self.path_sqlite))
        self.df_messages = pd.read_sql("SELECT * FROM ZWAMESSAGE", self.conn)
        self.df_chat_session = pd.read_sql(
            "SELECT * FROM ZWACHATSESSION", self.conn)
        self.df_profile_push_name = pd.read_sql(
            "SELECT * FROM ZWAPROFILEPUSHNAME", self.conn)
        self.df_media_item = pd.read_sql("SELECT * FROM ZWAMEDIAITEM", self.conn)
        self.df_group_member = pd.read_sql("SELECT * FROM ZWAGROUPMEMBER", self.conn)

        current_chat = self.df_messages.iloc[0]['ZCHATSESSION']
        chat_id, chat_name = self.__get_chat_id_name(current_chat)
        chat = self.add_chat(chat_id, chat_name)
        n = self.df_messages.shape[0]
        
        for i, item in enumerate(self.df_messages.sort_values(by=['ZCHATSESSION']).iterrows()):
            row = item[1]
            #print(row)
            #print(row['ZISFROMME'])
           
            progress(i, n)


            if row['ZMESSAGETYPE'] == 10: ##MENSAGENS TYPE == 10 SÃO INUTEIS, BROADCASTS E SYSTEM MENSAGENS
                continue

            if current_chat != row['ZCHATSESSION']:
                self.add(chat)
                chat_id, chat_name = self.__get_chat_id_name(
                    row['ZCHATSESSION'])
                chat = self.add_chat(chat_id, chat_name)
                current_chat = row['ZCHATSESSION']
            message = Message()
            jid, from_name = self.__get_from_name(row['ZFROMJID'], row['ZGROUPMEMBER'])
            if not row['ZISFROMME'] == 0:
                from_name = "Proprietário"
            

          
            # if is_from_me == 1:
            #     from_name = "Proprietário"

            message.from_ = self.add_participant(jid, from_name)
            if not message.from_ in chat.participants and message.from_:
                chat.participants.append(message.from_)
            message.timestamp = convert_timestamp(row['ZMESSAGEDATE'])
            message.read_source = self.read_source
            message.chat_id = chat.id
            message.body = row['ZTEXT']
            if row['ZMEDIAITEM']:
                res = self.add_file(row['ZMEDIAITEM'])
                if res:
                    file, title = res
                    file.message = message
                    message.body = title
                    self.add(file)
            self.add(message)
        self.commit()

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
            self.unknow_chat_count += 1
            chat = Chat()
            chat.identifier = f"Chat desconhecido {self.unknow_chat_count}"
            chat.name = f"Chat desconhecido {self.unknow_chat_count}"
            chat.read_source = self.read_source
            self.add(chat)
            self.commit()
        else:
            chat = db_session.query(Chat).filter(
                Chat.identifier == identifier, Chat.name == name).first()
            if not chat:
                chat = Chat()
                chat.identifier = identifier
                chat.name = name
                chat.read_source = self.read_source
                self.add(chat)
                self.commit()
        chat.source = "WhatsAPP Iphone"
        return chat

    def add_file(self, pk):
        try:
            df2 = self.df_media_item[self.df_media_item['Z_PK'] == pk]
            row = df2.iloc[0]
        except:
            return None
        if not row['ZMEDIALOCALPATH']:
            return
        path = Path(row['ZMEDIALOCALPATH'])
        file = db_session.query(File).filter(File.extracted_path == str(path)).first()
        if not file:
            file = File()
            file.name = path.name
            file.extracted_path = str(path)
            file.deleted_state = 'Intact'
            file.content_type = row['ZVCARDSTRING']
        return file, row['ZTITLE']


    def __get_from_name(self, fromjid, group_member_pk):
        try:
            df2 = self.df_group_member[self.df_group_member['Z_PK'] == group_member_pk]
            jid = df2.iloc[0]['ZMEMBERJID']
            df2 = self.df_profile_push_name[self.df_profile_push_name['ZJID'] == jid]
            return (jid, df2.iloc[0]['ZPUSHNAME'])
        except Exception as e:
            return (fromjid, None)
            

    def __get_chat_id_name(self, pk):
        try:
            df2 = self.df_chat_session[self.df_chat_session['Z_PK'] == pk]
            return (df2.iloc[0]['ZCONTACTJID'], df2.iloc[0]['ZPARTNERNAME'])
        except:
           return None, None
