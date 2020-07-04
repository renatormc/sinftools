from database import db_connect
from models import *
import os
import codecs
import re
from datetime import datetime


def chat_worker(kargs):
    obj = ChatWorker(read_source_id=kargs['read_source_id'],  exp=kargs['exp'],
                     chats_path=kargs['chats_path'], att_path=kargs['att_path'])
    obj.run(kargs['filename'])


class ChatWorker:

    def __init__(self, read_source_id,  exp, chats_path, att_path):
        self.read_source_id = read_source_id
        self.exp = exp
        self.chats_path = chats_path
        self.att_path = att_path

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

    def getChatsFilename(self):
        return os.listdir(self.chats_path)

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

    def run(self, filename):
        self.engine, self.db_session = db_connect()
        self.read_source = self.db_session.query(
            ReadSource).get(self.read_source_id)
        with codecs.open(os.path.join(self.chats_path, filename), 'r', 'utf-8') as f:
            text = f.read()

        chat = Chat()
        chat.name = os.path.basename(filename)
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
            attachment_regex = r'(.*\..{3,4}\s+){1}(?:\(.*\)){1}'
            regex_test = re.search(attachment_regex, msg.body)
            if regex_test:
                attachment_regex_valitade = r'(.*\..{3,4}\s+)'
                regex_test = re.search(attachment_regex, msg.body).groups()
                validate = re.search(
                    attachment_regex_valitade, regex_test[0])
                if validate:
                    validate = validate.string
                    validate = validate.strip()
                    validate = validate[1:]
                    validate = os.path.join(self.att_path, validate)
                    if os.path.exists(validate):
                        attachment = File()
                        attachment.extracted_path = str(Path(validate).relative_to(
                            self.read_source.folder)) if validate else None
                        attachment.filename = os.path.basename(
                            attachment.extracted_path)
                        attachment.size = os.path.getsize(validate)
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
        self.add(chat)
        self.commit()
        self.engine.dispose()
