import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *

#APAGUE TUDO QUE ESTÁ DAQUI PARA BAIXO E COLOQUE SEU CÓDIGO, MATENHA O QUE ESTÁ ACIMA
#Printar o identificador de todos os chats existentes
chats = db_session.query(Chat).all()
for chat in chats:
    print(chat.friendly_identifier)
