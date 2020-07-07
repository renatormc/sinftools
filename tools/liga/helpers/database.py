from models import *
from sqlalchemy import or_

def filter_depends_on(query, id):
    query = query.filter(or_(Process.dependencies.ilike(f"%[{id},%"), Process.dependencies.ilike(f"%,{id},%"), Process.dependencies.ilike(f"%,{id}]%")))
    return query