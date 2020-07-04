import shutil
import os
import time
from uuid import uuid4
import config
from pathlib import Path
import tempfile
from database import db_session
from models import *
from datetime import datetime


def set_connected(name):
    path = Path(tempfile.gettempdir()) / "sinftools_who_connected.txt"
    doc = db_session.query(Document).filter_by(key="who_connected").first()
    if not doc:
        doc = Document()
        doc.key = "who_connected"
    now = datetime.now()
    doc.value = {
        "name": name,
        "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
    }
    db_session.add(doc)
    db_session.commit()

def get_connected():
    doc = db_session.query(Document).filter_by(key="who_connected").first()
    if doc:
        return doc.value
    return {
        "name": "Alguém",
        "timestamp": "horário desconhecido"
    }
