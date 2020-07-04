from database import db_session
from models import *
# import jsonschema._reflect
import codecs
from config_manager import config_manager



class ProprietaryFinder:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        read_sources = db_session.query(ReadSource).all()
        
        apps = [item[0] for item in db_session.query(Chat).filter(Chat.read_source == self.read_source).with_entities(Chat.source).distinct()]
        for app in apps:
            statistic = {}
            n_chats = 0
            chats = db_session.query(Chat).filter(Chat.read_source == self.read_source, Chat.source == app).all()
            for chat in chats:
                if chat.participants.count() == 2:
                    n_chats += 1
                    for part in chat.participants:
                        try:
                            statistic[part.id] += 1
                        except KeyError:
                            statistic[part.id] = 1
            if statistic:
                items = [(key, value) for key, value in statistic.items()]
                res = max(items, key=lambda x: x[1])
                if res[1] >= 0.6*n_chats and n_chats > 2:
                    part = db_session.query(Participant).get(res[0])
                    part.proprietary = True
                    db_session.add(part)

        db_session.commit()
        


if __name__ == "__main__":
    pf = ProprietaryFinder()
    pf.run()
