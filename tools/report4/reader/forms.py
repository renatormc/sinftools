from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField, SelectField, ValidationError
from form_fields import SDateTimeField, SFileSizeField, STimeIntervalField
from wtforms.validators import Optional
from wtforms.widgets import TextInput
import re
from datetime import timedelta, datetime
import settings


def contains_validator(form, field):
    if field.data:
        if 'regex:' in field.data:
            try:
                regexp = field.data[6:]
                re.compile(regexp)
            except:
                raise ValidationError(
                    'O campo deve possuir uma expressão regular válida')


class ChatForm(FlaskForm):
    class Meta:
        locales = ['pt_PT', 'pt']

    identifier_contains = StringField(
        'Identificador contém', validators=[contains_validator])
    identifier_not_contains = StringField(
        'Identificador não contém', validators=[contains_validator])
    source_contains = StringField(
        'Fonte contém', validators=[contains_validator])
    source_not_contains = StringField(
        'Fonte não contém', validators=[contains_validator])
    n_messages_gt = IntegerField(
        'Número de mensagens maior que', validators=[Optional()])
    n_messages_lt = IntegerField(
        'Número de mensagens menor que', validators=[Optional()])
    order = HiddenField("Order", default="last_activity desc")
    btn_submit = SubmitField('Pesquisar')


class MessageForm(FlaskForm):
    body_contains = StringField(
        'Corpo contém', validators=[contains_validator])
    body_not_contains = StringField(
        'Corpo não contém', validators=[contains_validator])
    chat_identifier_contains = StringField(
        'Identificador do chat contém', validators=[contains_validator])
    chat_identifier_not_contains = StringField(
        'Identificador do chat não contém', validators=[contains_validator])
    from_contains = StringField(
        'Remetente contém', validators=[contains_validator])
    from_not_contains = StringField(
        'Remetente não contém', validators=[contains_validator])
    timestamp_start = SDateTimeField(
        'Carimbo de hora inicial (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    timestamp_end = SDateTimeField(
        'Carimbo de hora final (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    order = SelectField('Ordenar por', default="timestamp", choices=[(
        'timestamp asc', 'Horário crescente'), ('timestamp desc', 'Horário decrescente'),
        ('from asc', 'Remetente crescente'), ('from desc', 'Remetente decrescente')])
    chat_id = HiddenField("Chat id")
    btn_submit = SubmitField('Pesquisar')


class FileForm(FlaskForm):
    type_ = SelectField('Tipo', default="all", choices=[(
        'all', 'Todos'), ('image', 'Imagens'), ('video', 'Videos'), ('audio', 'Áudios'), ('file', 'Outros')])
    chat = SelectField('Bate-papo', default='all', choices=[
        ('all', 'Todos os arquivos'), ('chat', 'Somente anexos de bate-papo'),
        ('not_chat', 'Somente os que não são anexos de bate-papo')])
    name_contains = StringField('Nome contém', validators=[contains_validator])
    name_not_contains = StringField(
        'Nome não contém', validators=[contains_validator])
    size_gt = SFileSizeField('Tamanho maior que', validators=[Optional()])
    size_lt = SFileSizeField('Tamanho menor que', validators=[Optional()])
    corrupted = SelectField('Provavelmente corrompido', choices=[(
        'all', 'Todos'), ('corrupted', 'Corrompido'), ('not_corrupted', 'Não corrompido')])
    creation_time_start = SDateTimeField(
        'Data de criação inicial (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    creation_time_end = SDateTimeField(
        'Data de criação final (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    modified_time_start = SDateTimeField(
        'Data de modificação inicial (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    modified_time_end = SDateTimeField(
        'Data de modificação final (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    extracted_path_contains = StringField(
        'Caminho da extração contém', validators=[contains_validator])
    extracted_path_not_contains = StringField(
        'Caminho da extração não contém', validators=[contains_validator])
    original_path_contains = StringField(
        'Caminho original contém', validators=[contains_validator])
    original_path_not_contains = StringField(
        'Caminho original não contém', validators=[contains_validator])
    order = HiddenField("Order", default="filename asc")
    chat_id = HiddenField("Chat id")
    btn_submit = SubmitField('Pesquisar')


class SmsForm(FlaskForm):
    body_contains = StringField(
        'Corpo da mensagem contém', validators=[contains_validator])
    body_not_contains = StringField(
        'Corpo da mensagem não contém', validators=[contains_validator])
    folder_contains = StringField(
        'Pasta contém', validators=[contains_validator])
    folder_not_contains = StringField(
        'Pasta não contém', validators=[contains_validator])
    parties_contains = StringField(
        'Partes contém', validators=[contains_validator])
    parties_not_contains = StringField(
        'Partes não contém', validators=[contains_validator])
    timestamp_start = SDateTimeField(
        'Carimbo de hora inicial (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    timestamp_end = SDateTimeField('Carimbo de hora final (dd/mm/yyyy hh:mm:ss)',
                                   validators=[Optional()])

    order = HiddenField("Order", default="timestamp asc")
    btn_submit = SubmitField('Pesquisar')


class ContactForm(FlaskForm):
    name_contains = StringField('Nome contém')
    name_not_contains = StringField('Nome não contém')
    source_contains = StringField('Fonte contém')
    source_not_contains = StringField('Fonte não contém')
    entries_contains = StringField('Entradas contém')
    entries_not_contains = StringField('Entradas não contém')
    order = HiddenField("Order", default="name asc")
    btn_submit = SubmitField('Pesquisar')


class CallForm(FlaskForm):
    type_contains = StringField('Tipo contém', validators=[contains_validator])
    type_not_contains = StringField(
        'Tipo não contém', validators=[contains_validator])
    duration_gt = STimeIntervalField(
        'Duração maior que', validators=[Optional()])
    duration_lt = STimeIntervalField(
        'Duração menor que', validators=[Optional()])
    timestamp_start = SDateTimeField(
        'Carimbo de hora inicial (dd/mm/yyyy hh:mm:ss)', validators=[Optional()])
    timestamp_end = SDateTimeField('Carimbo de hora final (dd/mm/yyyy hh:mm:ss)',
                                   validators=[Optional()])

    order = HiddenField("Order", default="timestamp asc")
    btn_submit = SubmitField('Pesquisar')
