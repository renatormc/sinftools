from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, Text, Interval, \
    PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import json

from database import Base

chat_participant = Table('chat_participant', Base.metadata,
                         Column('chat', Integer, ForeignKey(
                             'chat.id'), nullable=False),
                         Column('participant', Integer, ForeignKey(
                             'participant.id'), nullable=False),
                         PrimaryKeyConstraint('chat', 'participant'))

tag_message = Table('tag_message', Base.metadata,
                    Column('tag', Integer, ForeignKey(
                        'tag.id'), nullable=False),
                    Column('message', Integer, ForeignKey(
                        'message.id'), nullable=False),
                    PrimaryKeyConstraint('tag', 'message'))

tag_chat = Table('tag_chat', Base.metadata,
                 Column('tag', Integer, ForeignKey('tag.id'), nullable=False),
                 Column('chat', Integer, ForeignKey(
                     'chat.id'), nullable=False),
                 PrimaryKeyConstraint('tag', 'chat'))

tag_sms = Table('tag_sms', Base.metadata,
                Column('tag', Integer, ForeignKey('tag.id'), nullable=False),
                Column('sms', Integer, ForeignKey('sms.id'), nullable=False),
                PrimaryKeyConstraint('tag', 'sms'))

tag_contact = Table('tag_contact', Base.metadata,
                    Column('tag', Integer, ForeignKey(
                        'tag.id'), nullable=False),
                    Column('contact', Integer, ForeignKey(
                        'contact.id'), nullable=False),
                    PrimaryKeyConstraint('tag', 'contact'))

tag_call = Table('tag_call', Base.metadata,
                 Column('tag', Integer, ForeignKey('tag.id'), nullable=False),
                 Column('call', Integer, ForeignKey(
                     'call.id'), nullable=False),
                 PrimaryKeyConstraint('tag', 'call'))

tag_file = Table('tag_file', Base.metadata,
                 Column('tag', Integer, ForeignKey('tag.id'), nullable=False),
                 Column('file', Integer, ForeignKey(
                     'file.id'), nullable=False),
                 PrimaryKeyConstraint('tag', 'file'))


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    color = Column(String(30))
    can_delete = Column(Boolean, nullable=False, default=True)
    messages = relationship('Message', secondary=tag_message,
                            back_populates='tags', lazy='dynamic')
    chats = relationship('Chat', secondary=tag_chat,
                         back_populates='tags', lazy='dynamic')
    smss = relationship('Sms', secondary=tag_sms,
                        back_populates='tags', lazy='dynamic')
    calls = relationship('Call', secondary=tag_call,
                         back_populates='tags', lazy='dynamic')
    contacts = relationship('Contact', secondary=tag_contact,
                            back_populates='tags', lazy='dynamic')
    files = relationship('File', secondary=tag_file,
                         back_populates='tags', lazy='dynamic')


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey('participant.id'))
    from_ = relationship('Participant', backref='messages')
    timestamp = Column(DateTime)
    body = Column(Text)
    deleted_state = Column(String(50))
    user_message = Column(Boolean, nullable=False, default=False)
    color = Column(String(30))
    page_renderized = Column(Integer)
    tag_id = Column(Integer, ForeignKey('tag.id'))
    chat_id = Column(Integer, ForeignKey('chat.id'))
    analise_attachment_types = Column(String(50), nullable=False, default="")
    attachments = relationship('Attachment', backref='message', lazy='dynamic')
    tags = relationship('Tag', secondary=tag_message,
                        back_populates='messages', lazy='dynamic')


class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    identifier = Column(String(100))
    friendly_identifier = Column(String(100))
    name = Column(String(100))
    start_time = Column(DateTime)
    last_activity = Column(DateTime)
    n_messages = Column(Integer, nullable=False, default=0)
    participants = relationship(
        'Participant', secondary=chat_participant, back_populates='chats', lazy='dynamic')
    messages = relationship('Message', backref='chat', lazy='dynamic')
    deleted_state = Column(String(50))
    source = Column(String(50))
    avatar = Column(String(100))
    tags = relationship('Tag', secondary=tag_chat,
                        back_populates='chats', lazy='dynamic')


class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    identifier = Column(String(100))
    friendly_identifier = Column(String(100))
    name = Column(String(100))

    chats = relationship('Chat', secondary=chat_participant,
                         back_populates='participants', lazy='dynamic')
    avatar = Column(String(100))


class Sms(Base):
    __tablename__ = 'sms'
    id = Column(Integer, primary_key=True)
    body = Column(Text)
    timestamp = Column(DateTime)
    status = Column(String(50))
    folder = Column(String(50))
    deleted_state = Column(String(50))
    parties = relationship('SmsPart', backref='smss', lazy='dynamic')
    tags = relationship('Tag', secondary=tag_sms,
                        back_populates='smss', lazy='dynamic')


class SmsPart(Base):
    __tablename__ = 'sms_part'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    identifier = Column(String(100))
    name = Column(String(100))
    deleted_state = Column(String(50))
    sms_id = Column(Integer, ForeignKey('sms.id'))


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    deleted_state = Column(String(50))
    source = Column(String(50))
    entries = relationship("ContactEntry", backref='contact', lazy='dynamic')
    tags = relationship('Tag', secondary=tag_contact,
                        back_populates='contacts', lazy='dynamic')


class ContactEntry(Base):
    __tablename__ = 'contact_entry'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    category = Column(String(100))
    value = Column(String(200))
    deleted_state = Column(String(50))


class Call(Base):
    __tablename__ = 'call'
    id = Column(Integer, primary_key=True)
    type_ = Column(String(50))
    timestamp = Column(DateTime)
    duration = Column(Interval)
    deleted_state = Column(String(50))
    parties = relationship('CallPart', backref='call', lazy='dynamic')
    tags = relationship('Tag', secondary=tag_call,
                        back_populates='calls', lazy='dynamic')


class CallPart(Base):
    __tablename__ = 'call_part'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    identifier = Column(String(100))
    name = Column(String(100))
    call_id = Column(Integer, ForeignKey('call.id'))
    deleted_state = Column(String(50))


class Attachment(Base):
    __tablename__ = 'attchment'
    id = Column(Integer, primary_key=True)
    filename = Column(String(300))
    extracted_path = Column(String(400))
    meta_data = Column(String(200))
    content_type = Column(String(50))
    analise_thumb = Column(String(400))
    corrupted = Column(Boolean, nullable=False, default=False)
    type_ = Column(String(15), nullable=False, default='file')
    deleted_state = Column(String(50))
    message_id = Column(Integer, ForeignKey('message.id'))


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    original_path = Column(String(500))
    extracted_path = Column(String(500))
    content_type = Column(String(50))
    creation_time = Column(DateTime)
    modify_time = Column(DateTime)
    access_time = Column(DateTime)
    sha256 = Column(String(50))
    md5 = Column(String(50))
    deleted_state = Column(String(50))
    type_ = Column(String(50))
    page_renderized = Column(Integer)
    analise_thumb = Column(String(400))
    corrupted = Column(Boolean, nullable=False, default=False)
    tags = relationship('Tag', secondary=tag_file,
                        back_populates='files', lazy='dynamic')


class UserAccount(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(100))
    service_type = Column(String(100))
    password = Column(String(120))
    deleted_state = Column(String(50))


class Config(Base):
    __tablename__ = 'config'
    key = Column(String(100), primary_key=True)
    value = Column(Text)
    is_json = Column(Boolean, nullable=False, default=False)

    def get_value(self):
        if self.is_json:
            return json.loads(self.value) if self.value else {}
        return self.value

    def set_value(self, data):
        if isinstance(data, str):
            self.value = data
            self.is_json = False
            return
        self.value = json.dumps(data)
        self.is_json = True
