import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *
from sqlalchemy import text
from pathlib import Path
from helpers_processor import get_file_type

messages = db_session.query(Message).filter(Message.extra != text("'null'")).all()

for message in messages:
    text = message.extra[0]['filename']
    files = db_session.query(File).filter(File.filename.ilike(f'%{text}%')).all()
    if files and len(files) == 1:
        file = files[0]
        print(f"Renomeando arquivo {file.filename}")
        file.rename(text)
        file.type_ = get_file_type(file)
        db_session.add(file)
        message.attachments.append(file)
        db_session.add(message)
db_session.commit()
        
        
    
    
