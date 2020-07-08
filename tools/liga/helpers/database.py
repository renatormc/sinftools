from models import *
from database import db_session
from sqlalchemy import or_

def filter_depends_on(query, id):
    query = query.filter(or_(Process.dependencies.ilike(f"%[{id},%"), Process.dependencies.ilike(f"%,{id},%"), Process.dependencies.ilike(f"%,{id}]%")))
    return query

def get_contacts():
    db_session.query(User).order_by(User.name).all()