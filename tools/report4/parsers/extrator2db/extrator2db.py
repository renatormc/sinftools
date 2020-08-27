import os
from models import *
from database import db_session
from datetime import timedelta, datetime
from parsers.parser_base import ParserBase
from dateutil import parser
import re
from helpers_cmd import progress
from config_manager import config_manager
from multiprocessing import Pool
from parsers.extrator2db.workers import chat_worker


class ExtratorParser(ParserBase):
    def __init__(self):
        self.expressions = [
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{4})\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{4})?\s(\d{1,2}:\d{2}))', '%d/%m/%Y %H:%M'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2}))', '%d/%m/%y %H:%M'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\,\s(\d{1,2}:\d{2}))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\,\s(\d{1,2}:\d{2}))', '%d/%m/%y, %H:%M'),
            (r'(?P<timestamp>(\d{2}/\d{2}/\d{2})\s(\d{1,2}:\d{2} ((PM)|(AM))))\s?(-(?P<from>.*?):)?\s?(?P<body>.*)',
             r'((\d{2}/\d{2}/\d{2})?\s(\d{1,2}:\d{2} ((PM)|(AM))))', '%d/%m/%y %I:%M %p')
        ]
        self.exp = None
        self.map_files = {}

    def choose_exp(self):
        d = {item[0]: item for item in self.expressions}
        self.exp = d[self.read_source.regex_spi_tools]


    def scan_attachments(self):
        if not self.media_folder:
            return
        print("Analisando pasta de anexos")
        self.map_files = {}
        ref_folder = Path(self.read_source.folder).absolute()
        for p in self.media_folder.rglob("*"):
            try:
                self.map_files[p.name] = str(p.absolute().relative_to(ref_folder))
            except ValueError:
                print(f"Erro no arquivo \"{p.absolute()}\"")

       
    def check_env(self):
        msgs = []
        self.choose_exp()
        self.extrator_folder = Path(self.read_source.folder) / "EXTRATOR"
        self.media_folder = Path(self.read_source.folder) / "Media"
        if not self.media_folder.exists():
            print("Pasta Media não encontrada")
            self.media_folder = None
        if not self.extrator_folder.exists():
            msgs.append("Não foi encontrada uma pasta de nome EXTRATOR")
        return msgs

    def run(self):
        self.scan_attachments()
        self.lista = self.getChatsFolders()
        n = len(self.lista)
        print("Lendo chats")
        n_workers = config_manager.n_workers
        procs = ({'read_source_id': self.read_source.id, 'exp': self.exp, 'folder': f, 'map_files': self.map_files} for f in self.lista)
        if n_workers > 1:
            pool = Pool(processes=n_workers)
            for i, _ in enumerate(pool.imap_unordered(chat_worker, procs)):
                progress(i, n)
            pool.close()
            pool.join()
        else:
            for i, proc in enumerate(procs):
                chat_worker(proc)
                progress(i, n)
        

    def getChatsFolders(self):
        return [entry for entry in self.extrator_folder.iterdir() if entry.is_dir()]

 