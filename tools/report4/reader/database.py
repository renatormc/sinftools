from sqlalchemy import create_engine, event, engine
from sqlalchemy.orm import scoped_session, sessionmaker
import settings
import re

# engine, db_session, Base = None, None, None

# def db_connect():
#     global engine
#     global db_session
#     global Base
   
#     engine = create_engine(settings.database, convert_unicode=True)
#     if settings.database_type == 'sqlite' or settings.exec_mode == 'portable':
#         def sqlite_regexp(expr, item):
#             if item is None:
#                 return False
#             reg = re.compile(expr, re.I)
#             return reg.search(item) is not None

#         @event.listens_for(engine, "begin")
#         def do_begin(conn):
#             conn.connection.create_function('regexp', 2, sqlite_regexp)
#     db_session = scoped_session(sessionmaker(autocommit=False,
#                                             autoflush=False,
#                                             bind=engine))
#     Base = declarative_base()
#     Base.query = db_session.query_property()

def db_connect():
   
    engine = create_engine(settings.database, convert_unicode=True)
    if settings.database_type == 'sqlite' or settings.exec_mode == 'portable':
        def sqlite_regexp(expr, item):
            if item is None:
                return False
            reg = re.compile(expr, re.I)
            return reg.search(item) is not None

        @event.listens_for(engine, "begin")
        def do_begin(conn):
            conn.connection.create_function('regexp', 2, sqlite_regexp)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))
    return engine, db_session

engine, db_session = db_connect()

