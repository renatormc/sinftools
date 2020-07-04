from models import *
from database import db_session
from pathlib import Path

class GroupInfo:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print("Agrupando objetos")
        devices = db_session.query(Device).all()
        for device in devices:
            path = Path(device.folder)
            device.group = path.parent
            db_session.add(device)
        db_session.commit()