from sqlalchemy import create_engine, event, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, Text
from datetime import datetime


engine = create_engine(
    "sqlite:///bot.db", convert_unicode=True, encoding="utf-8")
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    start_extraction = Column(DateTime)
    end_extraction = Column(DateTime)

    def __repr__(self):
        return self.folder


def init_db():
    Base.metadata.create_all(bind=engine)


def get_or_new(name):
    chat = db_session.query(Chat).filter_by(name=name).first()
    if not chat:
        chat = Chat()
        chat.name = name
        db_session.add(chat)
        db_session.commit()
    return chat


def register_start_extraction(name):
    chat = get_or_new(name)
    chat.start_extraction = datetime.now()
    db_session.add(chat)
    db_session.commit()


def register_finish_extraction(name):
    chat = get_or_new(name)
    chat.end_extraction = datetime.now()
    db_session.add(chat)
    db_session.commit()


def has_been_tried(name):
    chat = db_session.query(Chat).filter_by(name=name).first()
    if chat and chat.start_extraction:
        return True
    return False

def has_been_extracted(name):
    chat = db_session.query(Chat).filter_by(name=name).first()
    if chat and chat.end_extraction:
        return True
    return False

def get_not_extracted():
    return db_session.query(Chat).filter(Chat.end_extraction == None).all()

def get_extracted():
    return db_session.query(Chat).filter(Chat.end_extraction != None).all()
    