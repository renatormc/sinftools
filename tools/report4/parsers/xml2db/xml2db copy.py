import os
from models import *
from datetime import timedelta
import xml.etree.ElementTree as ET
from dateutil import parser
from helpers_cmd import progress
import re
from parsers.parser_base import  ParserBase
from pathlib import Path


def duration_parse(duration_string):
    try:
        parts = duration_string.split(":")
        return timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))
    except:
        return None


class XmlParser(ParserBase):

    def __init__(self):
        pass

    def load(self):
        print("Carregando arquivo XML")
        self.tree = ET.parse( Path(self.read_source.folder) / self.read_source.data_file)
        self.root = self.tree.getroot()
        m = re.match('\{.*\}', self.root.tag)
        self.namespace = m.group(0) if m else ''

    def add_participant(self, identifier, name):
        participant = db_session.query(Participant).filter(Participant.identifier == identifier, Participant.name == name).first()
        if not participant:
            participant = Participant()
            participant.identifier = identifier
            participant.name = name
            self.add(participant)
            self.commit()
        return participant

    def check_env(self):
        msgs = []
        return msgs

    def run(self):
        self.load()
        self.parse_chats()
        self.parse_sms()
        self.parse_contact()
        self.parse_call()
        self.parse_files()
        self.parse_user_acccounts()

    def parse_chats(self):
        chats_el = self.root.find(f".//{self.namespace}modelType[@type='Chat']")
        if chats_el:
            n = len(chats_el)
            print("Lendo chats")
            for i, chat_el in enumerate(chats_el):
                progress(i, n)
                chat = Chat()

                chat.deleted_state = chat_el.attrib['deleted_state']

                field = chat_el.find(f"{self.namespace}field[@name='Id']")
                value = field.find(f"{self.namespace}value") if field else None
                chat.identifier = value.text if value is not None else ""

                field = chat_el.find(f"{self.namespace}field[@name='Name']")
                value = field.find(f"{self.namespace}value") if field else None
                chat.name = value.text if value is not None else ""

                field = chat_el.find(f"{self.namespace}field[@name='Source']")
                value = field.find(f"{self.namespace}value") if field else None
                chat.source = value.text if value is not None else ""

                field = chat_el.find(f"{self.namespace}field[@name='StartTime']")
                value = field.find(f"{self.namespace}value") if field else None
                chat.start_time = parser.parse(value.text) if value is not None else None

                field = chat_el.find(f"{self.namespace}field[@name='LastActivity']")
                value = field.find(f"{self.namespace}value") if field else None
                chat.last_activity = parser.parse(value.text) if value is not None else None

                field = chat_el.find(f"{self.namespace}multiModelField[@name='Participants']")
                for participant_el in field:
                    field = participant_el.find(f"{self.namespace}field[@name='Identifier']")
                    value = field.find(f"{self.namespace}value") if field else None
                    identifier = value.text if value is not None else None

                    field = participant_el.find(f"{self.namespace}field[@name='Name']")
                    value = field.find(f"{self.namespace}value") if field else None
                    name = value.text if value is not None else None
                    
                    participant = self.add_participant(identifier, name)
                    if not participant in chat.participants:
                        chat.participants.append(participant)

                field = chat_el.find(f"{self.namespace}multiModelField[@name='Messages']")
                if field:
                    for j, message_el in enumerate(field):
                        message = Message()

                        message.deleted_state = message_el.attrib['deleted_state']

                        field = message_el.find(f"{self.namespace}field[@name='Body']")
                        value = field.find(f"{self.namespace}value") if field else None
                        message.body = value.text if value is not None else None

                        field = message_el.find(f"{self.namespace}field[@name='TimeStamp']")
                        value = field.find(f"{self.namespace}value") if field else None
                        message.timestamp = parser.parse(value.text) if value is not None else None

                        from_el = message_el.find(f"{self.namespace}modelField[@name='From']").find(
                            f"{self.namespace}model")
                        from_identifier = from_name = None
                        if from_el:
                            field = from_el.find(f"{self.namespace}field[@name='Identifier']")
                            value = field.find(f"{self.namespace}value") if field else None
                            from_identifier = value.text if value is not None else None
                            field = from_el.find(f"{self.namespace}field[@name='Name']")
                            value = field.find(f"{self.namespace}value") if field else None
                            from_name = value.text if value is not None else None
                            message.from_ = self.add_participant(from_identifier, from_name)

                        attachments_el = message_el.find(f"{self.namespace}multiModelField[@name='Attachments']")
                        if attachments_el:
                            for attachment_el in attachments_el:
                                attachment = File()

                                attachment.deleted_state = attachment_el.attrib['deleted_state']

                                field = attachment_el.find(f"{self.namespace}field[@name='Filename']")
                                value = field.find(f"{self.namespace}value") if field else None
                                attachment.filename = value.text if value is not None else None

                                field = attachment_el.find(f"{self.namespace}field[@name='attachment_extracted_path']")
                                value = field.find(f"{self.namespace}value") if field else None
                                attachment.extracted_path = value.text if value is not None else None

                                field = attachment_el.find(f"{self.namespace}field[@name='ContentType']")
                                value = field.find(f"{self.namespace}value") if field else None
                                attachment.content_type = value.text if value is not None else None

                                field = attachment_el.find(f"{self.namespace}field[@name='MetaData']")
                                value = field.find(f"{self.namespace}value") if field else None
                                attachment.meta_data = value.text if value is not None else None

                                self.add(attachment)
                                message.attachments.append(attachment)
                        self.add(message)
                        chat.messages.append(message)
                    self.add(chat)
            self.commit()

    def parse_sms(self):
        smss_el = self.root.find(f".//{self.namespace}modelType[@type='SMS']")
        if smss_el:
            n = len(smss_el)
            print("\nLendo SMS")
            for i, sms_el in enumerate(smss_el):
                progress(i, n)
                sms = Sms()

                sms.deleted_state = sms_el.attrib['deleted_state']

                field = sms_el.find(f"{self.namespace}field[@name='TimeStamp']")
                value = field.find(f"{self.namespace}value") if field else None
                sms.timestamp = parser.parse(value.text) if value is not None else None

                field = sms_el.find(f"{self.namespace}field[@name='Folder']")
                value = field.find(f"{self.namespace}value") if field else None
                sms.folder = value.text if value is not None else None

                field = sms_el.find(f"{self.namespace}field[@name='Status']")
                value = field.find(f"{self.namespace}value") if field else None
                sms.status = value.text if value is not None else None

                field = sms_el.find(f"{self.namespace}field[@name='Body']")
                value = field.find(f"{self.namespace}value") if field else None
                sms.body = value.text if value is not None else None

                parts_el = sms_el.find(f"{self.namespace}multiModelField[@name='Parties']")
                if parts_el:
                    for part_el in parts_el:
                        part = SmsPart()
                        part.deleted_state = part_el.attrib['deleted_state']

                        field = part_el.find(f"{self.namespace}field[@name='Identifier']")
                        value = field.find(f"{self.namespace}value") if field else None
                        part.identifier = value.text if value is not None else None

                        field = part_el.find(f"{self.namespace}field[@name='Name']")
                        value = field.find(f"{self.namespace}value") if field else None
                        part.name = value.text if value is not None else None

                        field = part_el.find(f"{self.namespace}field[@name='Role']")
                        value = field.find(f"{self.namespace}value") if field else None
                        part.role = value.text if value is not None else None

                        self.add(part)
                        sms.parties.append(part)
                self.add(sms)
            self.commit()

    def parse_contact(self):
        contacts_el = self.root.find(f".//{self.namespace}modelType[@type='Contact']")
        if contacts_el:
            n = len(contacts_el)
            print("\nLendo Contatos")
            for i, contact_el in enumerate(contacts_el):
                progress(i, n)
                contact = Contact()

                contact.deleted_state = contact_el.attrib['deleted_state']

                field = contact_el.find(f"{self.namespace}field[@name='Name']")
                value = field.find(f"{self.namespace}value") if field else None
                contact.name = value.text if value is not None else None

                field = contact_el.find(f"{self.namespace}field[@name='Source']")
                value = field.find(f"{self.namespace}value") if field else None
                contact.source = value.text if value is not None else None

                entries_el = contact_el.find(f"{self.namespace}multiModelField[@name='Entries']")
                if entries_el:
                    for entry_el in entries_el:
                        entry = ContactEntry()

                        entry.deleted_state = entry_el.attrib['deleted_state']

                        field = entry_el.find(f"{self.namespace}field[@name='Category']")
                        value = field.find(f"{self.namespace}value") if field else None
                        entry.category = value.text if value is not None else None

                        field = entry_el.find(f"{self.namespace}field[@name='Value']")
                        value = field.find(f"{self.namespace}value") if field else None
                        entry.value = value.text if value is not None else None

                        self.add(entry)
                        # self.commit()
                        contact.entries.append(entry)
                self.add(contact)
            self.commit()

    def parse_call(self):
        calls_el = self.root.find(f".//{self.namespace}modelType[@type='Call']")
        if calls_el:
            n = len(calls_el)
            print("\nLendo chamadas")
            for i, call_el in enumerate(calls_el):
                progress(i, n)
                call = Call()

                call.deleted_state = call_el.attrib['deleted_state']

                field = call_el.find(f"{self.namespace}field[@name='Type']")
                value = field.find(f"{self.namespace}value") if field else None
                call.type_ = value.text if value is not None else None

                field = call_el.find(f"{self.namespace}field[@name='TimeStamp']")
                value = field.find(f"{self.namespace}value") if field else None
                call.timestamp = parser.parse(value.text) if value is not None else None

                field = call_el.find(f"{self.namespace}field[@name='Duration']")
                value = field.find(f"{self.namespace}value") if field else None
                call.duration = duration_parse(value.text) if value is not None else None

                parts_el = call_el.find(f"{self.namespace}multiModelField[@name='Parties']")
                if parts_el:
                    for part_el in parts_el:
                        part = CallPart()

                        part.deleted_state = part_el.attrib['deleted_state']

                        field = part_el.find(f"{self.namespace}field[@name='Identifier']")
                        value = field.find(f"{self.namespace}value") if field else None
                        part.identifier = value.text if value is not None else None

                        field = part_el.find(f"{self.namespace}field[@name='Name']")
                        value = field.find(f"{self.namespace}value") if field else None
                        part.name = value.text if value is not None else None

                        field = part_el.find(f"{self.namespace}field[@name='Role']")
                        value = field.find(f"{self.namespace}value") if field else None
                        part.role = value.text if value is not None else None

                        self.add(part)
                        call.parties.append(part)
                self.add(call)
            self.commit()

    def parse_files(self):
        tagged_fiels_el = self.root.find(f".//{self.namespace}taggedFiles")
        files_el = tagged_fiels_el.findall(f"{self.namespace}file") if tagged_fiels_el else None
        if files_el:
            n = len(files_el)
            print("\nLendo arquivos")
            for i, file_el in enumerate(files_el):
                progress(i, n)
                file_ = File()

                try:
                    file_.deleted_state = file_el.attrib['deleted']
                except:
                    file_.deleted_state = "Unknow"

                file_.original_path = file_el.attrib['path']

                file_.size = file_el.attrib['size']

                value = file_el.find(f".//{self.namespace}timestamp[@name='CreationTime']")
                file_.creation_time = parser.parse(value.text) if value is not None else None

                value = file_el.find(f".//{self.namespace}timestamp[@name='ModifyTime']")
                file_.modify_time = parser.parse(value.text) if value is not None else None

                value = file_el.find(f".//{self.namespace}timestamp[@name='AccessTime']")
                file_.access_time = parser.parse(value.text) if value is not None else None

                value = file_el.find(f".//{self.namespace}item[@name='Local Path']")
                file_.extracted_path =  value.text if value is not None else None

                value = file_el.find(f".//{self.namespace}item[@name='SHA256']")
                file_.sha256 = value.text if value is not None else None

                value = file_el.find(f".//{self.namespace}item[@name='MD5']")
                file_.md5 = value.text if value is not None else None

                value = file_el.find(f".//{self.namespace}item[@name='Tags']")
                file_.type_ = value.text.lower() if value is not None else None
                if file_.type_ and file_.type_ not in ['audio', 'image', 'video']:
                    file_.type = 'file'
                               

                value = file_el.find(f".//{self.namespace}item[@name='ContentType']")
                file_.content_type = value.text if value is not None else None

                self.add(file_)
            self.commit()

    def parse_user_acccounts(self):
        user_accounts_el = self.root.findall(f".//{self.namespace}model[@type='UserAccount']")
        if user_accounts_el:
            n = len(user_accounts_el)
            print("\nLendo contas de usuário")
            for i, user_account_el in enumerate(user_accounts_el):
                progress(i, n)
                user_account = UserAccount()

                user_account.deleted_state = user_account_el.attrib['deleted_state']

                field = user_account_el.find(f"{self.namespace}field[@name='Name']")
                value = field.find(f"{self.namespace}value") if field else None
                user_account.name = value.text if value is not None else None

                field = user_account_el.find(f"{self.namespace}field[@name='Username']")
                value = field.find(f"{self.namespace}value") if field else None
                user_account.username = value.text if value is not None else None

                field = user_account_el.find(f"{self.namespace}field[@name='Password']")
                value = field.find(f"{self.namespace}value") if field else None
                user_account.password = value.text if value is not None else None

                field = user_account_el.find(f"{self.namespace}field[@name='ServiceType']")
                value = field.find(f"{self.namespace}value") if field else None
                user_account.service_type = value.text if value is not None else None

                self.add(user_account)
            self.commit()

