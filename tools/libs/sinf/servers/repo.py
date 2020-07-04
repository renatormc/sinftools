from sinf.servers.models import *
from sinf.servers.database import db_session

def get_telegram_broken_url():
    doc = db_session.query(Document).filter_by(key="telegram_broken_url").first()
    if doc:
        return doc.value

def set_telegram_broken_url(value):
    doc = db_session.query(Document).filter_by(key="telegram_broken_url").first()
    if not doc:
        doc = Document()
        doc.key = "telegram_broken_url"
    doc.value = value
    db_session.add(doc)
    db_session.commit()