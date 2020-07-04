import os
from models import *
from database import db_session
from datetime import timedelta, datetime
from parsers.parser_base import ParserBase
from dateutil import parser
import re
from helpers_cmd import instruct_continue
import codecs
from helpers_cmd import progress
from config_manager import config_manager
from multiprocessing import Pool
from parsers.spi2db.workers import chat_worker


class SPIParser(ParserBase):
    def __init__(self):
        self.expressions = [
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{4})\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{4})?\s(\d{1,2}:\d{2}))', '%d/%m/%Y %H:%M'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2}))', '%d/%m/%y %H:%M'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\,\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\,\s(\d{1,2}:\d{2}))', '%d/%m/%y, %H:%M'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\s(\d{1,2}:\d{2} ((PM)|(AM))))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))', '%d/%m/%y %I:%M %p')
        ]
        self.percentual = 0.8
        self.exp = None

    def choose_exp(self):
        d = {item[0]: item for item in self.expressions}
        self.exp = d[self.read_source.regex_spi_tools]

    def read_chat(self, filename):
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
                except:
                    pass
            self.add(msg)
            chat.messages.append(msg)
        self.add(chat)
        self.commit()

    def check_env(self):
        msgs = []
        self.choose_exp()
        self.att_path = os.path.join(self.read_source.folder, "anexos_spi")
        self.chats_path = os.path.join(self.read_source.folder, "chats_spi")
        if not os.path.exists(self.chats_path):
            msgs.append(f"Não foi encontrada a pasta {self.chats_path}")
        if not os.path.exists(self.att_path):
            msgs.append(f"Não foi encontrada a pasta {self.att_path}")
        return msgs

    def run(self):

        # self.lista = self.getChatsFilename()
        # print("Lendo chats...")
        # n = len(self.lista)
        # for i, item in enumerate(self.lista):
        #     progress(i, n)
        #     self.read_chat(item)

        self.lista = self.getChatsFilename()
        n = len(self.lista)
        print("Lendo chats")
        pool = Pool(processes=config_manager.data['n_workers'])

        procs = ({'read_source_id': self.read_source.id, 'exp': self.exp,
                  'chats_path': self.chats_path, 'att_path': self.att_path, 'filename': f} for f in self.lista)
        for i, _ in enumerate(pool.imap_unordered(chat_worker, procs)):
            progress(i, n)
        pool.close()
        pool.join()

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
