from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
sinftools_dir = os.getenv("SINFTOOLS")
script_dir = os.path.dirname(os.path.realpath(__file__))
 
# engine = create_engine('mysql://root:808452@localhost/frasesprontas')
#engine = create_engine('mysql://root:iclrsinf@10.129.3.14:3306/frasesprontas')
engine = create_engine(f'sqlite:///{sinftools_dir}\\var\\banco.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
 
########################################################################
class Frase(Base):
    """"""
    __tablename__ = "frases"
 
    id = Column(Integer, primary_key=True)
    palavras_chave = Column(String(100))
    texto = Column(Text)
    
 
# create tables
Base.metadata.create_all(engine)