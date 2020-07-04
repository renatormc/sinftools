from models import *
from database import db_session
from pathlib import Path

class ProcessAvatars:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        self.rename_avatars()
        participants = db_session.query(Participant).filter_by(
            read_source_id=self.read_source.id).all()
        for participant in participants:
            participant.avatar = self.get_avatar(
                participant.identifier, self.read_source.folder)
            db_session.add(participant)

        chats = db_session.query(Chat).filter_by(read_source_id=self.read_source.id).all()
        for chat in chats:
            chat.avatar = self.get_avatar(
                chat.identifier, self.read_source.folder)
            db_session.add(chat)
        db_session.commit()

    def rename_avatars(self):
        folders = ['Avatars', 'Profile']
        for folder in folders:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    p = Path(folder, f)
                    if len(p.suffix) < 3:
                        p.rename(p.with_suffix('.jpg'))

    def get_avatar(self, identifier, device_folder):
        if not identifier:
            return
        identifier = self.get_short_identifier(identifier)
        folders = [os.path.join(device_folder, 'Avatars'), os.path.join(device_folder, 'Profile')]
        for folder in folders:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    if identifier in f:
                        return os.path.join(folder, f)

    def get_short_identifier(self, identifier):
        if "@s.whatsapp.net" in identifier or "@g.us" in identifier:
            return identifier.split("@")[0]
        elif "@" in identifier and "whatsapp" in identifier:
            parts = identifier.split("@")
            return parts[0]
        return identifier