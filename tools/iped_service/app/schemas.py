from marshmallow import Schema, fields
from models import *


class ProcessSchema(Schema):
        
    id = fields.Integer()
    name = fields.Str()
    perito = fields.Str()
    pid = fields.Integer()
    start = fields.DateTime(format="%d/%m/%Y %H:%M:%S")
    start_waiting = fields.DateTime(format="%d/%m/%Y %H:%M:%S")
    finish = fields.DateTime(format="%d/%m/%Y %H:%M:%S")
    status = fields.Str()
    output_folder = fields.Str()
    sources = fields.Str()
    profile = fields.Str()
    extra_params = fields.Str()
    iped_folder = fields.Str()
    queue_order = fields.Integer()