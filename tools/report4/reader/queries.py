from models import *
import shlex
from sqlalchemy import or_
# from helpers import convert_to_bytes, str2timedelta
from helpers_models import make_filter, unique_join

# if settings.exec_mode != 'portable':
#     import pandas as pd

regexop = "~*" if settings.database_type == 'postgres' else "regexp"


def contains(query, value, field):
    if value.startswith("regex:"):
        regexp = value[6:]
        query = query.filter(field.op(regexop)(regexp))
        return query
    if "%" in value:
        query = query.filter(field.ilike(value))
    else:
        parts = shlex.split(value)
        conditions = []
        for part in parts:
            conditions.append(field.ilike(f"%{part}%"))
        query = query.filter(or_(*conditions))
    return query


def not_contains(query, value, field):
    if value.startswith("regex:"):
        regexp = value[6:]
        query = query.filter(~field.op(regexop)(regexp))
        return query
    if "%" in value:
        query = query.filter(~field.ilike(value))
    else:
        parts = shlex.split(value)
        conditions = []
        for part in parts:
            conditions.append(field.ilike(f"%{part}%"))
        query = query.filter(~or_(*conditions))
    return query


# if settings.exec_mode != 'portable':
#     def get_queries_regex_chat_messages(query, expression):
#         q = query.with_entities(Message.id, Message.body)
#         df = pd.read_sql(q.statement, query.session.bind)
#         df2 = df[df.body.str.contains(expression, na=False)]
#         ids = list(df2.id)
#         return ids

def set_order(class_, value):
    parts = value.split(" ")
    return getattr(getattr(class_, parts[0]), parts[1])()


# ----------------------------------------------------------------------------------------


def chat_list(query, form):
    if form.identifier_contains.data:
        query = contains(query, form.identifier_contains.data,
                         Chat.friendly_identifier)
    if form.identifier_not_contains.data:
        query = not_contains(
            query, form.identifier_not_contains.data, Chat.friendly_identifier)
    if form.n_messages_gt.data:
        query = query.filter(Chat.n_messages > form.n_messages_gt.data)
    if form.n_messages_lt.data:
        query = query.filter(Chat.n_messages < form.n_messages_lt.data)
    if form.source_contains.data:
        query = contains(query, form.source_contains.data, Chat.source)
    if form.source_not_contains.data:
        query = not_contains(query, form.source_not_contains.data, Chat.source)
    # order
    if form.order.data == 'n_messages asc':
        query = query.order_by(Chat.n_messages.asc())
    elif form.order.data == 'n_messages desc':
        query = query.order_by(Chat.n_messages.desc())
    elif form.order.data == 'device asc':
        query = query.order_by(Device.folder.asc())
    elif form.order.data == 'device desc':
        query = query.order_by(Device.folder.desc())
    else:
        query = query.order_by(set_order(Chat, form.order.data))
    return query


def messages(query, form):
    if form.body_contains.data:
        query = contains(query, form.body_contains.data, Message.body)
    if form.body_not_contains.data:
        query = not_contains(query, form.body_not_contains.data, Message.body)
    if form.chat_identifier_contains.data:
        query = contains(query, form.chat_identifier_contains.data, Chat.friendly_identifier)
    if form.chat_identifier_not_contains.data:
        query = not_contains(query, form.chat_identifier_not_contains.data, Chat.friendly_identifier)
    if form.from_contains.data:
        query = query.join(Participant)
        query = contains(query, form.from_contains.data,
                         Participant.friendly_identifier)
    if form.from_not_contains.data:
        query = query.join(Participant)
        query = not_contains(query, form.from_not_contains.data,
                             Participant.friendly_identifier)
    if form.timestamp_start.data:
        query = query.filter(Message.timestamp >= form.timestamp_start.data)
    if form.timestamp_end.data:
        query = query.filter(Message.timestamp <= form.timestamp_end.data)
    if form.chat_id.data:
        query = query.filter(Message.chat_id == form.chat_id.data)
    if form.order.data == 'from asc':
        query = unique_join(query, Participant).order_by(
            Participant.friendly_identifier.asc())
    elif form.order.data == 'from desc':
        query = unique_join(query, Participant).order_by(
            Participant.friendly_identifier.desc())
    else:
        query = query.order_by(set_order(Message, form.order.data))
    return query


def smss(query, form):
    if form.body_contains.data:
        query = contains(query, form.body_contains.data, Sms.body)
    if form.body_not_contains.data:
        query = not_contains(query, form.body_not_contains.data, Sms.body)
    if form.folder_contains.data:
        query = contains(query, form.folder_contains.data, Sms.folder)
    if form.folder_not_contains.data:
        query = not_contains(query, form.folder_not_contains.data, Sms.folder)
    if form.parties_contains.data:
        query = query.filter(Sms.parties.any(or_(SmsPart.identifier.ilike(
            f"%{form.parties_contains.data}%"), SmsPart.name.ilike(f"%{form.parties_contains.data}%"))))
    if form.parties_not_contains.data:
        query = query.filter(~Sms.parties.any(or_(SmsPart.identifier.ilike(
            f"%{form.parties_contains.data}%"), SmsPart.name.ilike(f"%{form.parties_contains.data}%"))))
    if form.timestamp_start.data:
        query = query.filter(Sms.timestamp >= form.timestamp_start.data)
    if form.timestamp_end.data:
        query = query.filter(Sms.timestamp <= form.timestamp_end.data)
    query = query.order_by(set_order(Sms, form.order.data))
    return query


def contacts(query, form):
    if form.name_contains.data:
        query = contains(query, form.name_contains.data, Contact.name)
    if form.name_not_contains.data:
        query = not_contains(query, form.name_not_contains.data, Contact.name)
    if form.source_contains.data:
        query = contains(query, form.source_contains.data, Contact.source)
    if form.source_not_contains.data:
        query = not_contains(query, form.source_not_contains.data, Contact.source)
    if form.entries_contains.data:
        query = query.filter(Contact.entries.any(ContactEntry.value.ilike(f"%{form.entries_contains.data}%")))
    if form.entries_not_contains.data:
        query = query.filter(~Contact.entries.any(ContactEntry.value.ilike(f"%{form.entries_not_contains.data}%")))
    query = query.order_by(set_order(Contact, form.order.data))
    return query


def calls(query, form):
    if form.type_contains.data:
        query = contains(query, form.type_contains.data, Call.type_)
    if form.type_not_contains.data:
        query = not_contains(query, form.type_not_contains.data, Call.type_)
    if form.duration_gt.data:
        query = query.filter(Call.duration > form.duration_gt.data)
    if form.duration_lt.data:
        query = query.filter(Call.duration < form.duration_lt.data)
    if form.timestamp_start.data:
        query = query.filter(Call.timestamp >= form.timestamp_start.data)
    if form.timestamp_end.data:
        query = query.filter(Call.timestamp <= form.timestamp_end.data)
    query = query.order_by(set_order(Call, form.order.data))
    return query


def files(query, form):
    if form.name_contains.data:
        query = contains(query, form.name_contains.data, File.filename)
    if form.name_not_contains.data:
        query = not_contains(query, form.name_not_contains.data, File.filename)
    if form.size_gt.data:
        bytes_ = form.size_gt.data
        query = query.filter(File.size > bytes_)
    if form.size_lt.data:
        bytes_ = form.size_lt.data
        print(f"BYTES: {bytes_}")
        query = query.filter(File.size < bytes_)
    if form.corrupted.data:
        if form.corrupted.data == 'corrupted':
            query = query.filter(File.corrupted)
        elif form.corrupted.data == 'not_corrupted':
            query = query.filter(~File.corrupted)
    if form.creation_time_start.data:
        query = query.filter(File.creation_time >=
                             form.creation_time_start.data)
    if form.creation_time_end.data:
        query = query.filter(File.creation_time <= form.creation_time_end.data)
    if form.modified_time_start.data:
        query = query.filter(File.modify_time >= form.modified_time_start.data)
    if form.modified_time_end.data:
        query = query.filter(File.modify_time <= form.modified_time_start.data)
    if form.extracted_path_contains.data:
        query = contains(query, form.extracted_path_contains.data, File.extracted_path)
    if form.extracted_path_not_contains.data:
        query = not_contains(query, form.extracted_path_not_contains.data, File.extracted_path)
    if form.original_path_contains.data:
        query = contains(query, form.original_path_contains.data, File.original_path)
    if form.original_path_not_contains.data:
        query = not_contains(query, form.original_path_not_contains.data, File.original_path)
    if form.chat.data == 'chat':
        query = query.filter(File.message_id != None)
    elif form.chat.data == 'not_chat':
        query = query.filter(File.message_id == None)
    if form.type_.data != 'all':
        query = query.filter(File.type_ == form.type_.data)
    query = query.order_by(set_order(File, form.order.data))
    return query


class_dict = {
    'Chat': chat_list,
    'File': files,
    'Message': messages,
    'Sms': smss,
    'Contact': contacts,
    'Call': calls
}
