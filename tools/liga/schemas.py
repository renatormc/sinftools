from marshmallow import Schema, fields
from models import *
from pathlib import Path


class ProcessSchema(Schema):
        
    id = fields.Integer()
    script = fields.Str()
    perito = fields.Str()
    type = fields.Str()
    pid = fields.Integer()
    start = fields.DateTime(format="%d/%m/%Y %H:%M:%S")
    start_waiting = fields.DateTime(format="%d/%m/%Y %H:%M:%S")
    finish = fields.DateTime(format="%d/%m/%Y %H:%M:%S")
    status = fields.Str()
    depencies = fields.Function(lambda obj: obj.dependencies_ids)
    script_stem  = fields.Function(lambda obj: Path(obj.script).stem)
