import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *

files = db_session.query(File).filter(File.message_id != None, File.checked == False).all()
for file in files:
    message = file.message
    message.checked = False
    db_session.add(message)
db_session.commit()

