import abc
from database import db_session


class ParserBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError("Ainda não foi implementado o método 'run'")

    @abc.abstractmethod
    def check_env(self):
        raise NotImplementedError(
            "Ainda não foi implementado o método 'check_env'")

    @abc.abstractmethod
    def set_read_source(self, value):
        self.read_source = value

    @abc.abstractmethod
    def set_device(self, value):
        self.device = value

    @abc.abstractmethod
    def add(self, obj):
        obj.read_source_id = self.read_source.id
        db_session.add(obj)

    @abc.abstractmethod
    def commit(self):
        db_session.commit()
