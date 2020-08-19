from parsers.parser_base import ParserBase
import sqlite3
import pandas as pd
from datetime import datetime
import os
import sys
import shutil
from helpers_cmd import progress, instruct_continue
from models import *
from database import db_session
from parsers.sqlite2db.workers import hash_worker
from pathlib import Path
from multiprocessing import Pool
from config_manager import config_manager
from helpers_cmd import progress


def format_timestamp(value):
    try:
        return datetime.fromtimestamp(value/1000)
    except:
        return None


class Sqlite2Db(ParserBase):
    def __init__(self):
        pass

    def check_env(self):
        msgs = []
        self.path_msgstore = Path(self.read_source.folder) / "msgstore.db"
        self.path_wa = Path(self.read_source.folder) / "wa.db"
        if not self.path_msgstore.exists():
            msgs.append(
                f'Não foi encontrado o arquivo msgstore.db na pasta {self.read_source.folder}')
        if not self.path_wa.exists():
            msgs.append(
                f'Não foi encontrado o arquivo wa.db na pasta {self.read_source.folder}.')
        if msgs:
            return msgs
        self.attachments_folder = Path(self.read_source.folder) / "Media"
        if not self.attachments_folder.exists():
            msgs.append(
                f"Não foi encontrada a pasta \"{str(self.attachments_folder)}\"")
        self.folder_thumbs = Path(self.read_source.folder) / "thumbs_whatsapp"
        return msgs

    def run(self):
        if not os.path.exists(self.folder_thumbs):
            os.mkdir(self.folder_thumbs)
        self.connect_databases()
        self.calculate_hashes()
        self.chats_dict = {}
        self.parse_chats()

    def connect_databases(self):
        self.conn_msg = sqlite3.connect(str(self.path_msgstore))
        self.messages = pd.read_sql("SELECT * FROM messages", self.conn_msg)
        try:
            self.messages = self.messages[(
                self.messages['key_id'] != '-1') & (self.messages['key_remote_jid'] != '-1')]
        except:
            pass
        self.chat_list = pd.read_sql("SELECT * FROM chat_list", self.conn_msg)
        self.group_participants = pd.read_sql(
            "SELECT * FROM group_participants", self.conn_msg)
        self.conn_wa = sqlite3.connect(str(self.path_wa))
        self.contacts = pd.read_sql("SELECT * FROM wa_contacts", self.conn_wa)

    def calculate_hashes(self):
        self.hash_dict = {}
        print("Calculando hash dos arquivos na pasta de anexos")
        n_workers = config_manager.n_workers
        
        path = Path(self.attachments_folder)
        files = [path for path in path.glob('**/*') if path.is_file()]
        n = len(files)
        if n_workers > 1:
            pool = Pool(processes=n_workers)
            for i, data in enumerate(pool.imap_unordered(hash_worker, files)):
                progress(i, n)
                self.hash_dict[data[0]] = data[1]
            pool.close()
            pool.join()
        else:
            for i, file_ in enumerate(files):
                data = hash_worker(file_)
                progress(i, n)
                self.hash_dict[data[0]] = data[1]

        print("Hashes calculados")

    def get_participant(self, jid):
        df = self.contacts[self.contacts['jid'] == jid]
        if df.shape[0] > 0:
            aux = df.iloc[0]
            name = aux['display_name'] or aux['wa_name']
        else:
            name = jid
        return {'identifier': jid, 'name': name}

    def get_participants(self, row):
        jid = row['key_remote_jid']
        if "@g.us" in jid:
            parts = []
            df = self.group_participants[self.group_participants['gjid'] == jid]
            for i, row_ in df.iterrows():
                parts.append(self.get_participant(jid))
        else:
            parts = [{'identifier': 'Proprietário',
                      'name': 'Proprietário'}, self.get_participant(jid)]
        return parts

    def get_chat(self, jid):
        response = {'identifier': jid, 'name': None, 'start_time': None,
                    'last_activity': None, 'participants': []}
        df = self.chat_list[self.chat_list['key_remote_jid'] == jid]
        if df.shape[0] > 0:
            row = df.iloc[0]
            response['name'] = row['subject']
            response['start_time'] = format_timestamp(row['creation'])
            response['participants'] = self.get_participants(row)
        return response

    def extract_thumb(self, key_id):
        cursor = self.conn_msg.cursor()
        key_id_str = str(key_id)
        filename = key_id_str + ".jpg"
        path = os.path.join(self.folder_thumbs, filename)
        if os.path.exists(path):  # se já existe não extrai novamente
            return path
        res = cursor.execute(
            'select thumbnail from message_thumbnails where key_id = ' + "'" + key_id_str + "'").fetchall()
        if res:
            with open(path, "wb") as arq:
                arq.write(res[0][0])
            return path
        return None

    def get_attachment(self, row):
        response = {'size': None, 'mime_type': None, 'name': None,
                    'caption': None, 'hash': None, 'thumb': None, 'extracted_path': None}
        response['size'] = row['media_size']
        response['thumb'] = self.extract_thumb(row['key_id'])
        response['mime_type'] = row['media_mime_type']
        response['caption'] = row['media_caption']
        response['hash'] = row['media_hash']
        extracted_path = self.hash_dict[response['hash']] if response['hash'] in self.hash_dict.keys(
        ) else response['thumb']
        if not extracted_path:
            return None
        response['name'] = os.path.basename(extracted_path)
        response['extracted_path'] = extracted_path
        return response

    def get_messages(self):
        for i, row in self.messages.iterrows():
            mess = {'body': None, 'timestamp': None,
                    'from': None, 'chat': None, 'attachments': []}
            if not row['key_remote_jid'] in self.chats_dict:
                self.chats_dict[row['key_remote_jid']
                                ] = self.get_chat(row['key_remote_jid'])
            mess['body'] = row['data']
            mess['timestamp'] = format_timestamp(row['timestamp'])
            jid_from = row['remote_resource'] if "@g.us" in row['key_remote_jid'] else row['key_remote_jid']
            mess['from'] = self.get_participant(jid_from) if row['key_from_me'] == 0 else {
                'identifier': 'Proprietário', 'name': 'Proprietário'}
            mess['chat'] = self.chats_dict[row['key_remote_jid']]
            # verifica se tem anexo
            if row['media_mime_type'] or row['media_size'] or row['media_hash'] or row['thumb_image']:
                atts = self.get_attachment(row)
                mess['attachments'] = [atts] if atts else []
            yield mess

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

    def add_chat(self, chat_dict):
        if not chat_dict['identifier'] and not chat_dict['name']:
            return None
        chat = db_session.query(Chat).filter(
            Chat.identifier == chat_dict['identifier'], Chat.name == chat_dict['name']).first()
        if not chat:
            chat = Chat()
            chat.identifier = chat_dict['identifier']
            chat.name = chat_dict['name']
            chat.start_time = chat_dict['start_time']
            chat.source = self.read_source.chat_source
            for part in chat_dict['participants']:
                chat.participants.append(self.add_participant(
                    part['identifier'], part['name']))
            chat.deleted_state = "Intact"
            self.add(chat)
            self.commit()
        return chat

    def parse_chats(self):
        n = self.messages.shape[0]
        print("Lendo mensagens do sqlite")
        for i, mess in enumerate(self.get_messages()):
            progress(i, n)
            chat = self.add_chat(mess['chat'])
            message = Message()
            message.from_ = self.add_participant(
                mess['from']['identifier'], mess['from']['name'])
            message.body = mess['body']
            message.deleted_state = 'Intact'
            message.timestamp = mess['timestamp']
            message.chat_id = chat.id
            for att in mess['attachments']:
                attachment = File()
                attachment.filename = att['name']
                attachment.content_type = att['mime_type']
                attachment.size = att['size']
                attachment.extracted_path = os.path.relpath(
                    att['extracted_path'], self.read_source.folder)
                attachment.meta_data = att['caption']
                self.add(attachment)
                message.attachments.append(attachment)
            self.add(message)
        self.commit()
