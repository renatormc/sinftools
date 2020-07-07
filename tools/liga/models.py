import sqlalchemy as sa
from database import Base, init_db
from pathlib import Path
import config
from inflection import underscore
import os
import json
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100))
    telegram_chat_id = sa.Column(sa.Integer, nullable=False, default=-1)

    def __init__(self, *args, **kargs):
        super(User, self).__init__()
        for key, value in kargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.name

    


class Dependecy(Base):
    __tablename__ = 'dependency'
    id = sa.Column(sa.Integer, primary_key=True)
    blocked_id = sa.Column(sa.Integer, sa.ForeignKey("process.id"))
    blocker_id = sa.Column(sa.Integer, sa.ForeignKey("process.id"))
    blocked = relationship("Process", foreign_keys=[blocked_id], backref="dependencies_as_blocked")
    blocker = relationship("Process", foreign_keys=[blocker_id], backref="dependencies_as_blocker")

    def __str__(self):
        return f"{self.blocker_id}-{self.blocked_id}"


class Process(Base):
    __tablename__ = 'process'
    id = sa.Column(sa.Integer, primary_key=True)
    type = sa.Column(sa.String(50))
    script = sa.Column(sa.Text)
    perito = sa.Column(sa.String(300))
    pid = sa.Column(sa.Integer)
    start = sa.Column(sa.DateTime)
    start_waiting = sa.Column(sa.DateTime)
    finish = sa.Column(sa.DateTime)
    status = sa.Column(sa.String(50))
    stdout = sa.Column(sa.Text)
    stderr = sa.Column(sa.Text)
    params = sa.Column(sa.Text)
    telegram = sa.Column(sa.Boolean, nullable=False, default=False)

    def __str__(self):
        return self.script

    @property
    def dependencies_ids(self):
        try:
            return ",".join([str(dep.blocker.id) for dep in self.dependencies_as_blocked])
        except:
            return ""

    @property
    def dependencies(self):
        return [dep.blocker for dep in self.dependencies_as_blocked]

    def get_params(self):
        if self.params:
            return json.loads(self.params)

    def set_params(self, value):
        self.params = json.dumps(value)

    def generate_output_filenames(self):
        stem = underscore(Path(self.script).stem).replace(" ", "_")
        path_stdout = config.output_folder / f"{stem}_stdout.txt"
        path_stderr = config.output_folder / f"{stem}_stderr.txt"
        i = 1
        while path_stdout.exists() or path_stderr.exists():
            path_stdout = config.output_folder / f"{stem}_{i}_stdout.txt"
            path_stderr = config.output_folder / f"{stem}_{i}_stderr.txt"
            i += 1
        self.stdout = str(path_stdout)
        self.stderr = str(path_stderr)

    def delete_output_files(self):
        if self.stdout:
            path_stdout = Path(self.stdout)

            try:
                path_stdout.unlink()
            except (FileNotFoundError, PermissionError):
                pass
        if self.stderr:
            path_stderr = Path(self.stderr)
            try:
                path_stderr.unlink()
            except (FileNotFoundError, PermissionError):
                pass

    def get_output_tail(self, size=3000, stderr=False):
        try:
            path = self.stderr if stderr else self.stdout
            if not path:
                raise FileNotFoundError
            path = Path(path)
            file_size = path.stat().st_size
            offset = size if size <= file_size else file_size
            with path.open("rb") as f:
                f.seek(-offset, os.SEEK_END)
                data = f.read()
            # text = data.decode("cp1252")
            # text = data.decode("cp850")
            if self.type == "IPED":
                text = data.decode("cp1252")
            else:
                try:
                    text = data.decode("utf-8")
                except UnicodeDecodeError:
                    text = data.decode("cp850")
            return text
        except FileNotFoundError:
            return ""


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


init_db()