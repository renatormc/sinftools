import sqlalchemy as sa
from database import Base, init_db
from pathlib import Path
import config
from sqlalchemy.orm import relationship


class Caso(Base):
    __tablename__ = 'caso'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String(100))
    RG = sa.Column(sa.Integer)
    ano = sa.Column(sa.Integer)
    perito = sa.Column(sa.String(50))
    

    def __init__(self, *args, **kargs):
        super(Caso, self).__init__()
        
    def __str__(self):
        return self.caso


class Objeto(Base):
    __tablename__ = 'caso'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String(100))
    tipo = sa.Column(sa.String(100))
    caso = sa.Column(sa.Integer, sa.ForeignKey("caso.id"))
    

    def __init__(self, *args, **kargs):
        super(Caso, self).__init__()
        
    def __str__(self):
        return self.caso


class Tarefa(Base):
    __tablename__ = 'tarefa'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String(100))
    descricao = sa.Column(sa.Text)
    ordem = sa.Column(sa.Integer, nullable=False, default=0)
    objeto = sa.Column(sa.Integer, sa.ForeignKey("objeto.id"))
    

    def __init__(self, *args, **kargs):
        super(Caso, self).__init__()
        
    def __str__(self):
        return self.caso

    
