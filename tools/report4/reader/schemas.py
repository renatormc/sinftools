from flask_marshmallow import Marshmallow
from models import *

ma = Marshmallow()

class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag
        fields = ("name", "description", "color", "highlight")