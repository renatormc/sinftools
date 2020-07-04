import os
os.chdir(r'$cwd')
import sys
sys.path.insert(0, f'{os.getenv("SINFTOOLS")}\\tools\\report4')
from database import db_session
from models import *
from datetime import datetime
import pytz

from_ = "UTC"
to = "America/Sao_Paulo"

def convert_timezone(value, from_, to):
    if isinstance(value, datetime):
        from_ = pytz.utc if from_ == "UTC" else pytz.timezone(from_)
        to = pytz.utc if from_ == "UTC" else pytz.timezone(to)
        return value.replace(tzinfo=from_).astimezone(to)

messages = db_session.query(Message).all()
for message in messages:
    message.timestamp = convert_timezone(message.timestamp, from_, to)
    db_session.add(message)
smss = db_session.query(Sms).all()
for sms in smss:
    sms.timestamp = convert_timezone(sms.timestamp, from_, to)
    db_session.add(sms)
calls = db_session.query(Call).all()
for call in calls:
    call.timestamp = convert_timezone(call.timestamp, from_, to)
    db_session.add(call)
files = db_session.query(File).all()
for file in files:
    file.creation_time = convert_timezone(file.creation_time, from_, to)
    file.modify_time = convert_timezone(file.modify_time, from_, to)
    file.access_time = convert_timezone(file.access_time, from_, to)
    db_session.add(file)
chats = db_session.query(Chat).all()
for chat in chats:
    chat.start_time = convert_timezone(chat.start_time, from_, to)
    chat.last_activity = convert_timezone(chat.last_activity, from_, to)
    db_session.add(chat)
db_session.commit()