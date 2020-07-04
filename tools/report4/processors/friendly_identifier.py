from models import *
from database import db_session

class FriendlyIdentifier:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        self.genenerate_friendly_identifier_chat()
        self.genenerate_friendly_identifier_participant()

    def get_friendly_identifier(self, identifier, name):
        identifier = identifier.strip() if identifier else ""
        name = name.strip() if name else ""
        if name == identifier:
            name = ""
        number = ""
        if "@s.whatsapp" in identifier:
            number = identifier.split("@")[0] or ""
        elif "ONE_TO_ONE" in identifier:
            number = identifier.split(":")[1] or ""
        elif identifier and name:
            return f"{identifier} {name}"
        elif identifier:
            return identifier
        elif name:
            return name
        return f"{number} {name}" if name or number else "Desconhecido"

    def genenerate_friendly_identifier_chat(self):
        print("Gerando identificadores de chat")
        chats = db_session.query(Chat).filter_by(read_source_id=self.read_source.id).all()
        for chat in chats:
            chat.friendly_identifier = self.get_friendly_identifier(
                chat.identifier, chat.name)
            db_session.add(chat)
        db_session.commit()

    def genenerate_friendly_identifier_participant(self):
        print("Gerando identificadores de participantes")
        participants = db_session.query(Participant).filter_by(
            read_source_id=self.read_source.id).all()
        for participant in participants:
            participant.friendly_identifier = self.get_friendly_identifier(
                participant.identifier, participant.name)
            db_session.add(participant)
        db_session.commit()