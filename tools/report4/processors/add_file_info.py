from models import *
from database import db_session

class AddFileInfo:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print("Adicionando informação a arquivos")
        files = db_session.query(File).filter_by(read_source_id=self.read_source.id).all()
        for file_ in files:
            if file_.extracted_path:
                if not file_.filename:
                    file_.filename = os.path.basename(file_.extracted_path)
                path = file_.path
                if not file_.size and os.path.exists(path):
                    file_.size = os.path.getsize(file_.path)
                db_session.add(file_)
        db_session.commit()
