from models import *
from database import db_session
from pathlib import Path
import subprocess
import os


def delete_process(proc: Process):
    path = Path(proc.output_file)
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def get_disks():
    sinftools_dir = Path(os.getenv("SINFTOOLS"))
    ftkimager_path = sinftools_dir / "extras/ftkimager/ftkimager.exe"

    cmd = [str(ftkimager_path), "--list-drives"]

    process = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    out, err = process.communicate()
    text = err.decode("CP850")

    lines = text.split("\n")
    items = [line.strip() for line in lines if line.strip().startswith("\\\\")]
    return items


def get_last_dir():
    doc = db_session.query(Document).filter_by(key="last_dir").first()
    return doc.value if doc else "C:\\"


def set_last(path):
    path = Path(path)
    try:
        if path.is_file():
            path = path.parent
        doc = db_session.query(Document).filter_by(key="last_dir").first()
        if not doc:
            doc = Document()
            doc.key = "last_dir"
        doc.value = str(path)
        db_session.add(doc)
        db_session.commit()
    except FileNotFoundError:
        pass


def create_user_sinf():
    user = db_session.query(User).filter_by(name="sinf").first()
    if not user:
        user = User()
        user.name = "sinf"
        db_session.add(user)
        db_session.commit()