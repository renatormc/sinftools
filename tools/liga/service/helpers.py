import shutil
import os
import time
from uuid import uuid4
import config
from pathlib import Path
import tempfile
from database import db_session
from models import *
from datetime import datetime
from flask import make_response, jsonify
from werkzeug.utils import secure_filename
import zipfile


def set_connected(name):
    path = Path(tempfile.gettempdir()) / "sinftools_who_connected.txt"
    doc = db_session.query(Document).filter_by(key="who_connected").first()
    if not doc:
        doc = Document()
        doc.key = "who_connected"
    now = datetime.now()
    doc.value = {
        "name": name,
        "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
    }
    db_session.add(doc)
    db_session.commit()


def get_connected():
    doc = db_session.query(Document).filter_by(key="who_connected").first()
    if doc:
        return doc.value
    return {
        "name": "Alguém",
        "timestamp": "horário desconhecido"
    }


def get_telegram_broken_url():
    pass


def set_telegram_broken_url():
    pass


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


def save_profile(file):
    filename = secure_filename(file.filename)
    try:
        config.TEMPFOLDER.mkdir()
    except FileExistsError:
        pass
    zippath = config.TEMPFOLDER / filename
    file.save(str(zippath))
    folder = config.iped_folder / "profiles/pt-BR"
    old = folder.parent / f"{folder.name}.old"
    if old.exists():
        shutil.rmtree(old)
    if folder.exists():
        shutil.move(folder, old)
    with zipfile.ZipFile(str(zippath)) as zip_ref:
        zip_ref.extractall(folder)
    if old.exists():
        shutil.rmtree(old)
