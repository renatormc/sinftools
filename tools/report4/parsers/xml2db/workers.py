from database import db_connect
from models import *
from dateutil import parser


class ChatWorker:
    def __init__(self, read_source_id, namespace):
        self.read_source_id = read_source_id
        self.namespace = namespace
     
    def add(self, obj):
        obj.read_source_id = self.read_source_id
        self.db_session.add(obj)

    def commit(self):
        self.db_session.commit()

    def add_participant(self, identifier, name):
        participant = self.db_session.query(Participant).filter(Participant.identifier == identifier, Participant.name == name).first()
        if not participant:
            participant = Participant()
            participant.identifier = identifier
            participant.name = name
            self.add(participant)
            self.commit()
        return participant

    def run(self, chat_el):
        self.engine, self.db_session = db_connect()
    
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
        self.engine.dispose()


def chat_worker(kargs):
    obj = ChatWorker(read_source_id=kargs['read_source_id'], namespace=kargs['namespace'])
    obj.run(kargs['chat_el'])

class FilesWorker:
    def __init__(self, read_source_id, namespace):
        self.read_source_id = read_source_id
        self.namespace = namespace
     
    def add(self, obj):
        obj.read_source_id = self.read_source_id
        self.db_session.add(obj)

    def commit(self):
        self.db_session.commit()

    def run(self, chunk):
        self.engine, self.db_session = db_connect()
        for file_el in chunk:
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
            file_.type_ = value.text if value is not None else None
            file_.type_ = value.text.lower() if value is not None else None
            if file_.type_ and file_.type_ not in ['audio', 'image', 'video']:
                file_.type_ = 'file'

            value = file_el.find(f".//{self.namespace}item[@name='ContentType']")
            file_.content_type = value.text if value is not None else None
            self.add(file_)
        self.commit()
        self.engine.dispose()
    
def files_worker(kargs):
    obj = FilesWorker(read_source_id=kargs['read_source_id'], namespace=kargs['namespace'])
    obj.run(kargs['chunk'])