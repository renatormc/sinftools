from models import *
from database import db_session
from helpers import get_config
from pathlib import Path
from config_manager import config_manager
from helpers_processor import get_file_type

class FileType:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print("Deletando entradas com path de arquivo nulo")
        db_session.query(File).filter(File.extracted_path == None, File.message_id ==
                          None, File.read_source_id == self.read_source.id).delete()
        print("Atribuindo tipo aos arquivos")
        files = db_session.query(File).filter_by(read_source_id=self.read_source.id).filter(File.type_ == None).all() #somente arquivos que não tem tipo atribuido ainda
        for file_ in files:
            if file_.extracted_path:
                file_.type_ = get_file_type(file_)
                message = file_.message
                if message and file_.type_ not in message.analise_attachment_types:
                    message.analise_attachment_types += "/" + file_.type_
                    db_session.add(message)
            db_session.add(file_)
        db_session.query(File).filter_by(size=0).delete()
        db_session.commit()