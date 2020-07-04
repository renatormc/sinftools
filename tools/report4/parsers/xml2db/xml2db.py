import os
from models import *
from datetime import timedelta
import xml.etree.ElementTree as ET
from dateutil import parser
from helpers_cmd import progress
import re
from parsers.parser_base import  ParserBase
from pathlib import Path
from multiprocessing import Pool
from database import db_connect
from parsers.xml2db.workers import chat_worker, files_worker
from config_manager import config_manager


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

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
            pool = Pool(processes=config_manager.data['n_workers'])
            procs = ({'read_source_id': self.read_source.id, 'namespace': self.namespace, 'chat_el': chat_el} for chat_el in chats_el)
            for i, _ in enumerate(pool.imap_unordered(chat_worker, procs)):
                progress(i, n)
            pool.close()
            pool.join()
                     

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
            chunks_ = list(chunks(files_el, 50))
            n = len(chunks_)
            print("\nLendo arquivos")
            pool = Pool(processes=config_manager.data['n_workers'])
            procs = ({'read_source_id': self.read_source.id, 'namespace': self.namespace, 'chunk': chunk} for chunk in chunks_)
            for i, _ in enumerate(pool.imap_unordered(files_worker, procs)):
                progress(i, n)
            pool.close()
            pool.join()
                

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

