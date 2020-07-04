import sqlalchemy as sa
from database import Base
from pathlib import Path
import json


class Process(Base):
    __tablename__ = 'process'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(300))
    perito = sa.Column(sa.String(300))
    pid = sa.Column(sa.Integer)
    start = sa.Column(sa.DateTime)
    start_waiting = sa.Column(sa.DateTime)
    finish = sa.Column(sa.DateTime)
    status = sa.Column(sa.String(20))
    output_folder = sa.Column(sa.Text)
    sources = sa.Column(sa.Text)
    profile = sa.Column(sa.String(100))
    extra_params = sa.Column(sa.String(300))
    iped_folder = sa.Column(sa.String(500))
    queue_order = sa.Column(sa.Integer, nullable=False, default=0)

    def get_file_log(self) -> Path:
        return Path(self.output_folder) / "sinf.log"



    def __str__(self):
        return self.name


class Document(Base):
    __tablename__ = 'doc'
    id = sa.Column(sa.Integer, primary_key=True)
    key = sa.Column(sa.String(100))
    _value = sa.Column(sa.Text)

    @property
    def value(self):
        return json.loads(self._value)

    @value.setter
    def value(self, value):
        self._value = json.dumps(value)

    
