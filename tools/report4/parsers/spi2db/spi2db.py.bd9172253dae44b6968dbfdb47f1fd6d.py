import os
from models import *
from datetime import timedelta, datetime
from parsers.parser_base import ParserBase
from dateutil import parser
import re
from helpers_cmd import instruct_continue
import codecs
from helpers_cmd import progress
from PyInquirer import style_from_dict, Token, prompt, Separator

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

# This software was developed to parse SPI collected data from GB Whatsapp to s-report DB format


class SPIParser(ParserBase):
    def __init__(self):
        self.expressions = [
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))?\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))', '%d/%m/%y %I:%M %p'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{4})?\s(\d{1,2}:\d{2}))?\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{4})?\s(\d{1,2}:\d{2}))', '%d/%m/%Y %H:%M')
        ]
        self.percentual = 0.8
        self.exp = None
        # self.exp = r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))?\s?(-.*?:)?\s?(.*)'
        # self.exp_split_marker = r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))'
        self.att_path = "anexos_whatsapp_spi"
        self.chats_path = "conversas_whatsapp_spi"


    def choose_exp(self):
        exps = {item[1]: item for item in self.expressions}
        questions = [
            {
                'type': 'list',
                'message': 'Selecione uma expressão regular: ',
                'name': 'exp',
                'pageSize': 3,
                'choices': exps.keys()
            }
        ]
        res = prompt(questions, style=style)['exp']
        self.exp = exps[res]


    def read_chat(self, filename):
        with codecs.open(os.path.join(self.chats_path, filename), 'r', 'utf-8') as f:
            text = f.read()

        # Analisa qual das expressões regulares funcionam melhor
        lines = text.split("\n")
        n = len(lines)
        i = 0
        self.exp = None
        for exp in self.expressions:
            for line in lines:
                if re.match(exp[1], line):
                    i += 1
                if i/n >= self.percentual:
                    self.exp = exp
                    break
            if self.exp is not None:
                break

        if self.exp is not None:
            chat = Chat()
            chat.name = os.path.basename(filename)[:-4]
            chat.source = "Whatsapp"
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
                            attachment.extracted_path = str(validate)
                            attachment.filename = os.path.basename(
                                attachment.extracted_path)
                            attachment.size = os.path.getsize(
                                attachment.extracted_path)
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
        return msgs

    def run(self):
        if not os.path.exists(self.chats_path):
            os.mkdir(self.chats_path)
        if not os.path.exists(self.att_path):
            os.mkdir(self.att_path)
        instruct_continue(
            f"Mova os arquivos que tem o texto das mensagens para a pasta '{self.chats_path}' e os anexos para a pasta '{self.att_path}'")
        self.lista = self.getChatsFilename()
        print("Lendo chats...")
        n = len(self.lista)
        for i, item in enumerate(self.lista):
            print(f"\nLendo conversa '{item}'")
            progress(i, n)
            self.read_chat(item)

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

    # this must receive an array in the following scheme -> [(str) date_time, msg_from (str), msg(str)]
    # def populate_message_table(self, message_block):
    #     date = datetime.strptime(message_block[0], '%d/%m/%y %I:%M %p')
    #     participant = message_block[1]
    #     msg = message_block[2]

    def add_participant(self, identifier, name):
        participant = db_session.query(Participant).filter(
            Participant.identifier == identifier, Participant.name == name).first()
        if not participant:
            participant = Participant()
            participant.identifier = identifier
            participant.name = name
            self.add(participant)
            self.commit()
        return participant
