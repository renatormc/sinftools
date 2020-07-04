import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *

"""Deleta arquivos de extensões específicas"""
extensions = ['.gif', '.jpg']
files = db_session.query(File).filter(File.extension.in_([extensions])).all()
for file in files:
    file.checked = False
    db_session.add(file)
db_session.commit()
