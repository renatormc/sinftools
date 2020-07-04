from flask import Flask, send_from_directory, session
from models import *
from database import db_session
from views import views
from ajax import ajax
import settings
import os
from math import log2
from helpers_models import get_config, get_items_available
from helpers_http import random_id
from pathlib import Path
import urllib.request
import jinja_filters as jinja_filters
from helpers_http import url_for_local
from flask_bootstrap import Bootstrap
from schemas import ma

app = Flask(__name__)

app.secret_key = '!$%dfg'
app.register_blueprint(views)
app.register_blueprint(ajax)
Bootstrap(app)
app.items_available = get_items_available()
ma.init_app(app)


for name, function in jinja_filters.__dict__.items():
    app.jinja_env.filters[name] = function


@app.context_processor
def context():
    try:
        navbar_active = session['navbar_active']
    except KeyError:
        session['navbar_active'] = 'no'
        navbar_active = 'no'
    try:
        file_vizualization = session['file_vizualization']
    except KeyError:
        session['file_vizualization'] = 'table'
        file_vizualization = 'table'
    try:
        current_tag = db_session.query(Tag).get(session['current_tag_id'])
    except KeyError:
        current_tag = db_session.query(Tag).first()
        session['current_tag_id'] = current_tag.id

    n_highlights = db_session.query(Tag).filter_by(highlight = True).count()
       

    return dict(
        filters = get_config('filters'),
        all_devices = db_session.query(Device).all(),
        app_version=settings.app_version,
        items_available=app.items_available,
        url_for_local=url_for_local,
        all_tags=db_session.query(Tag).order_by(Tag.name.asc()).all(),
        current_tag=current_tag, 
        random_id=random_id, 
        navbar_active=navbar_active,
        file_vizualization=file_vizualization,
        n_highlights = n_highlights,
        exec_mode = settings.exec_mode, 
        settings=settings
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=settings.port, debug=True)
