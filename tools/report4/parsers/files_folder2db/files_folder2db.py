from parsers.parser_base import ParserBase
from helpers_cmd import progress, instruct_continue
from models import *
from database import db_session
import os
import hashlib
from datetime import datetime
from pathlib import Path

class FilesFolder2Db(ParserBase):
    def __init__(self):
        self.calculate_hash = False

    def check_env(self):
        msgs = []
        self.arquivos = Path(self.read_source.folder) / "arquivos_"
        if not self.arquivos.exists():
            msgs.append(f'A pasta "{self.arquivos}" não foi encontrada.')
        return msgs

    def sha256(self, fname):
        hash_sha256 = hashlib.sha256()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def md5(self, fname):
        md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def run(self):       
        n_files = sum([len(files) for r, d, files in os.walk(self.read_source.folder)])
        i = 0
        for root, dirs, files in os.walk(self.read_source.folder):
            if root == '.report':
                continue
            for f in files:
                path = os.path.join(root, f)
                file_ = File()
                file_.size = os.path.getsize(path)
                file_.filename = f
                file_.extracted_path = os.path.relpath(path, self.read_source.folder)
                try:
                    file_.creation_time = datetime.fromtimestamp(os.path.getctime(path))
                except:
                    file_.creation_time = None
                try:
                    file_.modify_time = datetime.fromtimestamp(os.path.getmtime(path))
                except:
                    file_.modify_time = None
                try:
                    file_.access_time = datetime.fromtimestamp(os.path.getatime(path))
                except:
                    file_.access_time = None
                if self.calculate_hash:
                    file_.sha256 = self.sha256(path)
                    file_.md5 = self.md5(path)
                file_.deleted_state = 'Intact'
                self.add(file_)
                i += 1
                progress(i, n_files)
        self.commit()

