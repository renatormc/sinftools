from models import *
from database import db_session

class Translations:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        self.translate_call()
        self.translate_sms()

    def translate_sms(self):
        print("Traduzindo SMS")
        smss = db_session.query(Sms).filter_by(read_source_id=self.read_source.id).all()
        for sms in smss:
            sms.folder = str(sms.folder).replace("Drafts", "Rascunhos")
            sms.folder = str(sms.folder).replace("Inbox", "Caixa de entrada")
            sms.folder = str(sms.folder).replace("Sent", "Enviadas")
            sms.folder = str(sms.folder).replace("Outbox", "Caixa de saída")
            db_session.add(sms)
        db_session.commit()

    def translate_call(self):
        print("Traduzindo chamadas")
        calls = db_session.query(Call).filter_by(read_source_id=self.read_source.id).all()
        for call in calls:
            call.type_ = str(call.type_).replace("Unknown", "Desconhecido")
            call.type_ = str(call.type_).replace("Outgoing", "Efetuada")
            call.type_ = str(call.type_).replace("Missed", "Perdida")
            call.type_ = str(call.type_).replace("Incoming", "Recebida")
            db_session.add(call)
        db_session.commit()