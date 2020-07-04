from sinf.extractors.classes import Contact, Sms, Call
import sqlite3
from datetime import datetime, timedelta

def getContacts_1(db):
    contacts = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT display_name, tokens FROM raw_contacts AS r LEFT JOIN search_index AS s ON s.contact_id = r._id")
    res = cursor.fetchall()
    for row in res:
        contact = Contact()
        contact.name = row[0]
        if row[1]:
            contact.entries = row[1].split(" ")
        contact.source = 'logs'
        contact.deleted = ""
        contacts.append(contact)
    return contacts

def getSmss_1(db):
    types = {
        1: "Recebida",
        2: "Enviada"
    }
    smss = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT address, content, date, box_type FROM messages")
    res = cursor.fetchall()
    for row in res:
        sms = Sms()
        sms.contact = row[0]
        if row[3] in types.keys():
            sms.type = types[row[3]]
        else:
            sms.type = row[3]
        sms.time = datetime.fromtimestamp(row[2] / 1e3)
        sms.body = row[1]
        sms.deleted = ""
        smss.append(sms)
    return smss

def getCalls_1(db):
    types = {
        1: "-",
        2: "-",
        3: "-",
        4: "-",
        5: "-"
    }
    calls = []
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT number, date, duration, type, name FROM logs WHERE sim_id = 0")
    res = cursor.fetchall()
    for row in res:
        call = Call()
        call.contact = f"{row[0]}-{row[4] if row[4] is not None else ''}"
        call.timestamp = datetime.fromtimestamp(row[1] / 1e3)
        call.duration = timedelta(seconds=row[2])
        if row[3] in types.keys():
            call.type = types[row[3]]
        else:
            call.type = row[3]
        call.deleted = ""
        calls.append(call)
    return calls