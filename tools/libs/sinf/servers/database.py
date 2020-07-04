from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sinf.servers import config
# from pymongo import MongoClient


# mongo = MongoClient('mongodb://10.129.3.14:27017/')

def db_connect():
    engine = create_engine(config.database_url, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
    return engine, db_session

try:
    engine, db_session = db_connect()
except Exception as e:
    print(e)
    engine, db_session = None, None
                    
Base = declarative_base()
# Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)

init_db()

