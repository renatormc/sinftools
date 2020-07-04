from models import *
from database import db_session
from helpers_processor import get_avatar, rename_avatars

class ChatRename:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        rename_avatars()
        participants = db_session.query(Participant).filter_by(
            read_source_id=self.read_source.id).all()
        for participant in participants:
            participant.avatar = get_avatar(
                participant.identifier, self.read_source.folder)
            db_session.add(participant)

        chats = db_session.query(Chat).filter_by(read_source_id=self.read_source.id).all()
        for i, chat in enumerate(chats):
            print(f"Renomeando chat '{i+1}'")
            n = chat.participants.count()
            if n == 1:
                part = chat.participants[0]
                if not part.proprietary:
                    chat.friendly_identifier = part.friendly_identifier
                    db_session.add(chat)
            elif n == 2:
                for part in chat.participants:
                    if not part.proprietary:
                        chat.friendly_identifier = part.friendly_identifier
                        db_session.add(chat)
            else:
                pass
        db_session.commit()