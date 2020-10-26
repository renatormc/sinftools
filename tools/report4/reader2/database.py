from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
import re

engine = create_engine("sqlite:///.report/db.db", convert_unicode=True, encoding="utf-8")


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
