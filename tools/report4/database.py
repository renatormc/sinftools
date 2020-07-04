from sqlalchemy import create_engine, event, engine
from sqlalchemy.orm import scoped_session, sessionmaker
import settings
import re
from config_manager import config_manager

localdb = config_manager.is_localdb()

   
def db_connect():
    url = config_manager.get_database_url()
    if url:
        engine = create_engine(config_manager.get_database_url(), convert_unicode=True)
        if config_manager.database_type == 'sqlite':
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


def init_db():
    import models
    import helpers
    engine, db_session = db_connect()

    models.Base.metadata.create_all(bind=engine)
    tag_highlight = models.Tag()
    tag_highlight.name = "Tag 1"
    tag_highlight.color = "#00aabb"
    db_session.add(tag_highlight)
    tag_exclude = models.Tag()
    tag_exclude.name = "Tag 2"
    tag_exclude.color = "#bc5a45"
    db_session.add(tag_exclude)
    
    config = models.Config()
    config.key = "workdir"
    config.set_value(str(settings.work_dir))
    db_session.add(config)
    db_session.commit()



   


   