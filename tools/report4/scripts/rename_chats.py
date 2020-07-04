import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *
# import helpers_scripts as hs

"""Este script renomeia os identificadores de cada chat baseado nos seus participantes
Antes de executá-lo não esqueça de abrir o arquivo de configurações e informar o nome do proprietário.
O que o script vai fazer é contar quantos participantes tem no chat, se for 1 ou 2 vai verificar se aquele não é o proprietário
se não for então mudará o nome do chat para o nome daquele participante (o que não é o proprietário). Se for mais de 2 participantes
não irá fazer nenhuma alteração'
"""

chats = db_session.query(Chat).all()
for i, chat in enumerate(chats):
    print(f"Analisando chat '{i+1}'")
    n = chat.participants.count()
    if n == 1:
        part = chat.participants[0]
        if not part.proprietary:
            chat.friendly_identifier = part.friendly_identifier
            db_session.add(chat)
    elif n == 2:
        for part in chat.participants:
            if not part.proprietary:
                chat.friendly_identifier = part.friendly_identifier
                db_session.add(chat)
    else:
        pass
db_session.commit()