import os
os.chdir(r'$cwd')
import sys
sinftools_dir = os.getenv("SINFTOOLS")
sys.path.insert(0, f'{sinftools_dir}\\tools\\report4')
from database import db_session
from models import *
import helpers_scripts as hs



print("Deletando arquivos que são anexos de mensagens que não estão marcados mas pertencem a mensagens que estão marcadas")
query = db_session.query(File).filter(File.checked != True,
                        File.message.has(Message.checked))
n = query.count()
if n > 0:
    options = {
        'Manter estes arquivos': 'not_delete',
        'Deletar mesmo assim': 'delete',
    }
    res = hs.show_options_cancel(
        f"Foram encontrados {n} arquivos que não estão marcados mas que são anexos de mensagens que estão marcadas. O que deseja fazer?", options=options)
    if res == 'delete':
        
        for file in query.all():
            message = file.message
            if not message.chat_id in chats_affected:
                chats_affected.append(message.chat_id)
            message.attachments.remove(file)
            if message.attachments.count() == 0 and not message.body:
                db_session.delete(message)
            file.delete_file()
            db_session.delete(file)
            
        db_session.commit()
       


print("Deletando arquivos que são anexos de mensagens que não estão marcadas")
query = db_session.query(File).filter(File.message_id != None,
                        File.message.has(Message.checked != True))
for file in query.all():
    file.delete_file()
    db_session.delete(file)
db_session.commit()


print("Deletando arquivos que são anexos de mensagens que pertencem a chats que não estão marcados")
query = db_session.query(File).filter(File.message_id != None,
                        File.message.has(Message.chat.has(Chat.checked != True)))
for file in query.all():
    file.delete_file()
    db_session.delete(file)
db_session.commit()

print("arquivos que não são anexos de mensagens e que não estão marcados")
query = db_session.query(File).filter(File.message_id == None, File.checked != True)
for file in query.all():
    file.delete_file()
    db_session.delete(file)
db_session.commit()

print("Deletando chats não marcados")
query = db_session.query(Chat).filter(Chat.checked != True)
for chat in query.all():
    chat.participants = []
    db_session.add(chat)
    db_session.delete(chat)
db_session.commit()


print("Deletando contatos, chamadas, sms e mensagens de chat")
classes = [Contact, Call, Sms, Message]
for class_ in classes:
    db_session.query(class_).filter(class_.checked != True).delete(
        synchronize_session=False)
db_session.commit()

print("Deletando participantes orfãos")
db_session.query(Participant).filter(~Participant.chats.any(
), ~Participant.messages.any()).delete(synchronize_session=False)


print("Recontando mensagens de chats")
for chat in db_session.query(Chat).all():
    chat.n_messages = chat.messages.count()
    db_session.add(chat)
db_session.commit()

print("Deletando chats vazios")
for chat in db_session.query(Chat).filter(Chat.n_messages == 0).all():
    db_session.delete(chat)
db_session.commit()