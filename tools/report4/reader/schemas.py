from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from models import *

ma = Marshmallow()

class TagSchema(ModelSchema):
    class Meta:
        model = Tag
        fields = ("name", "description", "color", "highlight")