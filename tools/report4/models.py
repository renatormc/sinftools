from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, Text, Interval, \
    PrimaryKeyConstraint, select, func, BigInteger
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
import json
import settings
import os
from pathlib import Path
from passlib.hash import pbkdf2_sha256
from urllib.parse import quote
from sqlalchemy.ext.declarative import declarative_base
from config_manager import config_manager

Base = declarative_base()


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
    description = Column(Text)
    highlight = Column(Boolean, nullable=False, default=False)
    color = Column(String(30))
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

    def count_items(self):
        return self.messages.count() + self.chats.count() + self.smss.count() + self.calls.count() + self.contacts.count() + self.files.count()


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True)
    folder = Column(String(300))
    group = Column(String(300))
    checked = Column(Boolean, nullable=False, default=True)
    read_sources = relationship('ReadSource', backref='device', lazy='dynamic')

    def __repr__(self):
        return self.folder


class ReadSource(Base):
    __tablename__ = 'read_source'
    id = Column(Integer, primary_key=True)
    folder = Column(String(300))
    process = Column(Boolean, nullable=False, default=True)
    data_file = Column(String(300))
    source_type = Column(String(300))
    regex_spi_tools = Column(String(300))
    chat_source =  Column(String(300), nullable=False, default="-")
    device_id = Column(Integer, ForeignKey('device.id'))

    def __repr__(self):
        return self.folder


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey('participant.id'))
    from_ = relationship('Participant', backref='messages')
    timestamp = Column(DateTime)
    # body = Column(Text(4294000000))
    body = Column(Text)
    deleted_state = Column(String(50))
    color = Column(String(30))
    page_renderized = Column(Integer)
    chat_id = Column(Integer, ForeignKey('chat.id'))
    analise_attachment_types = Column(String(50), nullable=False, default="")
    attachments = relationship('File', backref='message', lazy='dynamic')
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'messages', cascade="all, delete-orphan"))
    checked = Column(Boolean, nullable=False, default=True)
    _extra = Column(Text)
    tags = relationship('Tag', secondary=tag_message,
                        back_populates='messages', lazy='dynamic')

    @hybrid_property
    def extra(self):
        return json.loads(self._extra)

    @extra.setter
    def extra(self, value):
        self._extra = json.dumps(value)



class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    # identifier = Column(Text(4294000000))
    # friendly_identifier = Column(Text(4294000000))
    identifier = Column(Text)
    friendly_identifier = Column(Text)
    name = Column(String(300))
    start_time = Column(DateTime)
    last_activity = Column(DateTime)
    n_messages = Column(Integer, nullable=False, default=0)
    participants = relationship(
        'Participant', secondary=chat_participant, back_populates='chats', lazy='dynamic')
    messages = relationship('Message', backref='chat', lazy='dynamic', cascade="all, delete-orphan"
                            )
    deleted_state = Column(String(50))
    source = Column(String(50))
    avatar = Column(String(300))
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'chats', cascade="all, delete-orphan"))
    checked = Column(Boolean, nullable=False, default=True)
    tags = relationship('Tag', secondary=tag_chat,
                        back_populates='chats', lazy='dynamic')

    @hybrid_property
    def avatar_path(self):
        path = Path(settings.work_dir, self.avatar) if self.avatar else None
        if path and path.exists() and path.is_file():
            return Path(self.avatar)
        return settings.unknow_avatar
    

    @hybrid_property
    def avatar_link(self):
        p = Path(self.avatar_path).abspath().as_uri
        return Path(self.avatar_path).abspath().as_uri


class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    # identifier = Column(Text(4294000000))
    # friendly_identifier = Column(Text(4294000000))
    # name = Column(Text(4294000000))
    identifier = Column(Text)
    friendly_identifier = Column(Text)
    name = Column(Text)
    proprietary = Column(Boolean, nullable=False, default=False)
    chats = relationship('Chat', secondary=chat_participant,
                         back_populates='participants', lazy='dynamic')
    avatar = Column(String(300))
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'participants', cascade="all, delete-orphan"))

    @hybrid_property
    def avatar_path(self):
        path = Path(settings.work_dir, self.avatar) if self.avatar else None
        if path and path.exists() and path.is_file():
            return Path(self.avatar)
        return settings.unknow_avatar

    @hybrid_property
    def avatar_link(self):
        return Path(self.avatar_path).abspath().as_uri


class Sms(Base):
    __tablename__ = 'sms'
    id = Column(Integer, primary_key=True)
    # body = Column(Text(4294000000))
    body = Column(Text)
    timestamp = Column(DateTime)
    status = Column(String(50))
    folder = Column(String(50))
    deleted_state = Column(String(50))
    parties = relationship('SmsPart', backref='smss', lazy='dynamic')
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'smss', cascade="all, delete-orphan"))

    checked = Column(Boolean, nullable=False, default=True)
    tags = relationship('Tag', secondary=tag_sms,
                        back_populates='smss', lazy='dynamic')


class SmsPart(Base):
    __tablename__ = 'sms_part'
    id = Column(Integer, primary_key=True)
    role = Column(String(100))
    # identifier = Column(Text(4294000000))
    # name = Column(Text(4294000000))
    identifier = Column(Text)
    name = Column(Text)
    deleted_state = Column(String(50))
    sms_id = Column(Integer, ForeignKey('sms.id'))
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'sms_parts', cascade="all, delete-orphan"))


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    deleted_state = Column(String(50))
    source = Column(String(300))
    entries = relationship("ContactEntry", backref='contact', lazy='dynamic')
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'contacts', cascade="all, delete-orphan"))

    checked = Column(Boolean, nullable=False, default=True)
    tags = relationship('Tag', secondary=tag_contact,
                        back_populates='contacts', lazy='dynamic')


class ContactEntry(Base):
    __tablename__ = 'contact_entry'
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    category = Column(String(300))
    value = Column(Text)
    deleted_state = Column(String(50))
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'contact_entries', cascade="all, delete-orphan"))


class Call(Base):
    __tablename__ = 'call'
    id = Column(Integer, primary_key=True)
    type_ = Column(String(50))
    timestamp = Column(DateTime)
    duration = Column(Interval)
    deleted_state = Column(String(50))
    parties = relationship('CallPart', backref='call', lazy='dynamic')
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'calls', cascade="all, delete-orphan"))

    checked = Column(Boolean, nullable=False, default=True)
    tags = relationship('Tag', secondary=tag_call,
                        back_populates='calls', lazy='dynamic')


class CallPart(Base):
    __tablename__ = 'call_part'
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    # identifier = Column(Text(4294000000))
    # name = Column(Text(4294000000))
    identifier = Column(Text)
    name = Column(Text)
    call_id = Column(Integer, ForeignKey('call.id'))
    deleted_state = Column(String(50))
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'call_parts', cascade="all, delete-orphan"))


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    size = Column(BigInteger)
    filename = Column(Text)
    original_path = Column(String(1000))
    extracted_path = Column(String(1000))
    converted_path = Column(String(1000))
    extension = Column(String(300))
    content_type = Column(String(300))
    creation_time = Column(DateTime)
    modify_time = Column(DateTime)
    access_time = Column(DateTime)
    sha256 = Column(String(300))
    md5 = Column(String(300))
    deleted_state = Column(String(50))
    type_ = Column(String(50))
    page_renderized = Column(Integer)
    analise_thumb = Column(String(1000))
    message_id = Column(Integer, ForeignKey('message.id'))
    chat_included = Column(Boolean)
    corrupted = Column(Boolean, nullable=False, default=False)
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    read_source = relationship('ReadSource', backref=backref(
        'files', cascade="all, delete-orphan"))

    checked = Column(Boolean, nullable=False, default=True)
    tags = relationship('Tag', secondary=tag_file,
                        back_populates='files', lazy='dynamic')

    @hybrid_property
    def has_thumb(self):
        thumb_path = self.thumb_path
        if thumb_path and thumb_path.exists():
            return True
        return False
               

    @hybrid_property
    def path(self):
        path = self.converted_path or self.extracted_path
        if path:
            return Path(self.read_source.folder) / path

    @hybrid_property
    def thumb_path(self):
        if self.analise_thumb:
            return Path(self.read_source.folder) / "sinf_thumbs" / self.analise_thumb


    @hybrid_property
    def link(self):
        return quote(str(self.path).replace("\\", "/"))


    def delete_file(self):
        if self.extracted_path:
            path = Path(self.read_source.folder) / self.extracted_path
            if path.exists():
                path.unlink()
        if self.converted_path:
            path = Path(self.read_source.folder) / self.converted_path
            if path.exists():
                path.unlink()

    def rename(self, new_name):
        path = self.path
        extracted_path = Path(self.extracted_path)
        new_path = path.parent / new_name
        if path.exists():
            path.rename(new_path)
        self.extracted_path = str(extracted_path.parent / new_name)
        self.filename = new_name
               


class UserAccount(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    username = Column(Text)
    service_type = Column(String(500))
    password = Column(String(500))
    deleted_state = Column(String(50))
    read_source_id = Column(Integer, ForeignKey('read_source.id'))
    checked = Column(Boolean, nullable=False, default=True)
    read_source = relationship('ReadSource', backref=backref(
        'user_accounts', cascade="all, delete-orphan"))


class Config(Base):
    __tablename__ = 'config'
    key = Column(String(300), primary_key=True)
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
