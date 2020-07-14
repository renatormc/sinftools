import mongoengine as me
import datetime
import config

# MongoDB URI-style connect
me.connect(host=config.MONGO_URI)


class Caso(me.Document):
    nome = me.StringField(max_length=50, required=True)
    pericia = me.StringField(max_length=50)
    perito = me.StringField(max_length=50)


class TipoObjeto(me.Document):
    nome = me.StringField(max_length=50, required=True)


class Objeto(me.Document):
    nome = me.StringField(max_length=50, required=True)
    caso = me.StringField(max_length=50, required=True)
    tipo = me.StringField(max_length=50, required=True)
    anotacoes = me.StringField()
    local = me.StringField(max_length=100)
    perito = me.StringField(max_length=50)


class Tarefa(me.Document):
    objeto = me.StringField(max_length=50, required=True)
    nome = me.StringField(max_length=50, required=True)
    descricao = me.StringField()

    # date_modified = me.DateTimeField(default=datetime.datetime.utcnow)
