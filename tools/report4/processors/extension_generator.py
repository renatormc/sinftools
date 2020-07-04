from models import *
from database import db_session
from pathlib import Path

class ExtensionGenerator:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print(f"Analisando extensões dos arquivos, fonte: {self.read_source.folder}")
        files = db_session.query(File).filter(File.read_source == self.read_source).all()
        for file in files:
            if file.extracted_path:
                file.extension = Path(file.extracted_path).suffix.lower()
                db_session.add(file)
        db_session.commit()