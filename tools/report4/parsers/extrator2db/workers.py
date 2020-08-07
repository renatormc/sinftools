from database import db_connect
from models import *
import os
import codecs
import re
from datetime import datetime
from pathlib import Path


def chat_worker(kargs):
    obj = ChatWorker(read_source_id=kargs['read_source_id'],  exp=kargs['exp'])
    obj.run(kargs['folder'])


class ChatWorker:

    def __init__(self, read_source_id,  exp):
        self.read_source_id = read_source_id
        self.exp = exp
       

    def add(self, obj):
        obj.read_source_id = self.read_source_id
        self.db_session.add(obj)

    def commit(self):
        self.db_session.commit()

    def add_participant(self, identifier, name):
        participant = self.db_session.query(Participant).filter(
            Participant.identifier == identifier, Participant.name == name).first()
        if not participant:
            participant = Participant()
            participant.identifier = identifier
            participant.name = name
            self.add(participant)
            self.commit()
        return participant

    def line2message(self, message):
        result = re.search(self.exp[0], message, flags=re.DOTALL)
        if result:
            timestamp = result.group('timestamp')
            from_ = result.group('from')
            body = result.group('body')
            return {
                'timestamp': timestamp.strip() if timestamp else '',
                'from': from_.strip() if from_ else '',
                'body': body.strip() if body else ''
            }

    def find_txt_file(self, folder: Path) -> Path:
        for entry in folder.iterdir():
            if entry.is_file() and entry.name.startswith("CHAT_") and entry.suffix == ".txt":
                return entry


    def get_attachment(self, folder, text):
        attachment_regex = r'(.*\..{3,4}\s+){1}(?:\(.*\)){1}'
        regex_test = re.search(attachment_regex, text)
        if regex_test:
            attachment_regex_valitade = r'(.*\..{3,4}\s+)'
            regex_test = re.search(attachment_regex, text).groups()
            validate = re.search(
                attachment_regex_valitade, regex_test[0])
            if validate:
                validate = validate.string
                validate = validate.strip()
                validate = validate[1:]
                validate = folder / validate if validate else None
                if validate and validate.exists():
                    return validate

    def __get_chat_name(self, folder):
        folder = Path(folder)
        path = folder / "RELATORIO_EXTRATOR.txt"
        try:
            lines = path.read_text(encoding="utf-8").split("\n")
            return lines[1].replace("Conversa do WhatsApp com", "").strip()
        except (FileNotFoundError, IndexError):
            return folder.name.replace("Conversa do WhatsApp com", "").strip()

    def run(self, folder: Path):
        self.engine, self.db_session = db_connect()
        self.read_source = self.db_session.query(
            ReadSource).get(self.read_source_id)
        
        txt_file = self.find_txt_file(folder)
        if not txt_file:
            raise Exception(f"Na pasta {folder} não foi encontrado um arquivo que começa com CHAT_ e termina com .txt")
        with txt_file.open("r", encoding="utf-8") as f:
            text = f.read()
        chat = Chat()
        chat.name = self.__get_chat_name(folder)
        chat.source = self.read_source.chat_source
        chat.deleted_state = "Intact"
        self.add(chat)

        message_text = re.sub(self.exp[1], r'<!@#$%>\1', text)
        splitted_text = message_text.split('<!@#$%>')[1:]
        for msg_raw in splitted_text:
            result = self.line2message(msg_raw)
            if not result:
                continue
            msg = Message()
            if result['from']:
                p = self.add_participant(
                    result['from'], result['from'])  # participante
                msg.from_ = p
                if not p in chat.participants:
                    chat.participants.append(p)
            msg.body = result['body']
            msg.deleted_state = "Intact"
            attach = self.get_attachment(folder, msg.body)
            if attach:
                attachment = File()
                attachment.extracted_path = str(attach.relative_to(self.read_source.folder))
                attachment.filename = os.path.basename(attachment.extracted_path)
                attachment.size = os.path.getsize(attach)
                self.add(attachment)
                msg.attachments.append(attachment)
        
            if result['timestamp']:
                try:
                    date = datetime.strptime(
                        result['timestamp'], self.exp[2])
                    msg.timestamp = date
                except Exception as e:
                    print(e)
            self.add(msg)
            chat.messages.append(msg)
            self.commit()
        self.add(chat)
        self.commit()
        self.engine.dispose()
