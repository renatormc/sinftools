import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *
from datetime import datetime
from sqlalchemy import and_

#%% Desmarcar chats que não tem mensagens em um intervalo de tempo específico
data_inicial = datetime(2018, 2, 21, 0,0,0)
data_final = datetime(2018, 11, 30, 23,59,59)
message_condition = and_(Message.timestamp >= data_inicial, Message.timestamp <= data_final)
chats = db_session.query(Chat).filter(~Chat.message.any(message_condition)).all()
for chat in chats:
    chat.checked = False
    db_session.add(chat)
db_session.commit()

# Desmarcar também as mensagens
messages = db_session.query(Message).filter(message_condition).all()
for message in messages:
    message.checked = False
    db_session.add(message)
db_session.commit()
