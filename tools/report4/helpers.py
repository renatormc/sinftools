from flask import url_for, current_app
import traceback
import sys
import settings
import math
from database import db_session
from models import *
import json
from sqlalchemy import or_, desc
import pathlib
import urllib.request
import os
# import queries
from unicodedata import normalize
import re
from datetime import datetime
import json
import codecs
import ruamel.yaml
import uuid


class ResourceData:
    def __init__(self):
        self.search_data = {}
        self.resource = ""
        self.extra_data = {}
        self.page = 1
        self.items = []
        self.per_page = 100
        self.pages = 0
        self.total_items = 0
        self.classname = ""
        self.template = ""
        self.only_result = False
        self.search_form_template = ""
        self.page_title = ""
        self.offset_page = 0
        self.extra = None
        self.container_fluid = False


def parse_resource_string(value):
    parts = value.split("?")
    params = {}
    if len(parts) == 2:
        params_items = parts[1].split("&")
        for param_item in params_items:
            pieces = param_item.split("=")
            params[pieces[0]] = pieces[1]
    return {'name': parts[0], 'params': params}



def get_chat_sources_list():
    query = make_filter(Chat).with_entities(Chat.source)
    items = [item[0] for item in query.distinct()]
    sources = [{'source_name': item,
                'user_identifier': get_user_app(item)} for item in items]
    return sources


def get_user_app(name):
    user_account = db_session.query(UserAccount).filter(
        UserAccount.service_type.ilike(f"%{name}%")).first()
    if user_account:
        if user_account.username:
            return user_account.username
        if user_account.name:
            return user_account.name
    return ''


def get_chat_sources(query=None):
    if not query:
        query = make_filter(Chat)
    query = query.with_entities(Chat.source)
    items = [item[0] for item in query.distinct()]
    return items


def get_config(key):
    config = db_session.query(Config).filter_by(key=key).first()
    return config.get_value()


def set_config(key, value):
    config = db_session.query(Config).filter_by(key=key).first()
    if not config:
        config = Config()
        config.key = key
    config.set_value(value)
    db_session.add(config)
    db_session.commit()


def printError(e):
    text = ""
    ex_type, ex_value, ex_traceback = sys.exc_info()
    trace_back = traceback.extract_tb(ex_traceback)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
    text += "Exception type : %s " % ex_type.__name__
    text += "<br>Exception message : %s" % ex_value
    text += "<br>" + "\n".join(stack_trace)
    return text


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def get_page(query, per_page, page=1, only_count=False, gen_links=False):
    if isinstance(query, dict):
        qtd = len(query['ids'])
    else:
        qtd = query.count()
    total = int(qtd / per_page)
    if qtd % per_page != 0:
        total += 1
    if only_count:
        return total
    first_element = (page - 1) * per_page
    if isinstance(query, dict):
        rest = len(query['ids']) - first_element
        last_element = first_element + per_page
        n = len(query['ids'])
        if last_element > n:
            last_element = n
        page_ids = query['ids'][first_element:last_element]
        items = []
        class_ = query['class_']
        for chunk in chunks(page_ids, 100):
            q = db_session.query(class_).filter(class_.id.in_(chunk))
            items += q.all()
    else:
        items = query.offset(first_element).limit(per_page).all()

    # Make links to other pages
    links = []
    if gen_links:
        n_around = 4
        first = page - n_around
        if first < 1:
            first = 1
        last = page + n_around + 1
        if last > total:
            last = total
        disabled = True if page == first else False
        links.append({'page': 1, "html": "<<",
                      "active": False, 'disabled': disabled})
        links.append({'page': page - 1, "html": "<",
                      "active": False, 'disabled': disabled})
        for i in range(first, last + 1):
            active = i == page
            links.append(
                {'page': i, "html": i, "active": active, 'disabled': False})
        disabled = True if page == last else False
        links.append({'page': page + 1, "html": ">",
                      "active": False, 'disabled': disabled})
        links.append({'page': total, "html": ">>",
                      "active": False, 'disabled': disabled})

    return {
        "total_items": qtd,
        "items": items,
        "page": page,
        "pages": total,
        "per_page": per_page,
        "links": links,
        "query": query.offset(first_element).limit(per_page)
    }


def getErrorString(e):
    message = ""
    ex_type, ex_value, ex_traceback = sys.exc_info()
    trace_back = traceback.extract_tb(ex_traceback)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    text = "Exception type : %s " % ex_type.__name__
    message += "<br>" + text
    text = "Exception message : %s" % ex_value
    message += "<br>" + text
    text = "<br>".join(stack_trace)
    message += "<br>" + text
    return message


def delete_tag_helper(id):
    tag = db_session.query(Tag).get(id)
    if tag and tag.name not in ['Destaque', 'Excluir']:
        db_session.delete(tag)
        db_session.commit()


def url_for_local(relative_path):
    if not relative_path:
        return None
    path = urllib.request.pathname2url(relative_path)
    url = url_for("workdir", relative_path=path)
    return f"{current_app.config['MAIN_URL']}{url}"


def url_for_avatar(relative_path):
    if not relative_path or not os.path.exists(relative_path):
        return None
    relative_path = os.path.join(
        'html_files', 'Avatars', relative_path) if relative_path else ''
    return url_for_local(relative_path)


def url_for_class(class_name):
    if class_name in ['Sms', 'Contact', 'Call', 'Chat']:
        return url_for("views.items", class_name=class_name)
    return url_for("views.{}s".format(class_name.lower()))


def class_name(obj):
    return obj.__class__.__name__


def clean_text(txt):
    aux = normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'\s+', '_', aux).lower()


class ColorClassManager:
    def __init__(self):
        self.current_color = 1
        self.current_from_id = None

    def get_class_color(self, from_id):
        if not self.current_from_id:
            self.current_from_id = from_id
        if from_id != self.current_from_id:
            self.current_color = 1 if self.current_color == 5 else self.current_color + 1
            self.current_from_id = from_id
        return f"rm-color-{self.current_color}"


def get_items_available():
    items = []
    if db_session.query(Chat).count() > 0:
        items.append("chat")
    if db_session.query(Sms).count() > 0:
        items.append("sms")
    if db_session.query(Contact).count() > 0:
        items.append("contact")
    if db_session.query(Call).count() > 0:
        items.append("call")
    if db_session.query(File).filter(File.type_ == 'image').count() > 0:
        items.append("image")
    if db_session.query(File).filter(File.type_ == 'audio').count() > 0:
        items.append("audio")
    if db_session.query(File).filter(File.type_ == 'video').count() > 0:
        items.append("video")
    return items


def strmaxsize(value, maxsize, begin=True):
    if len(value) > maxsize:
        return value[:maxsize] + "..." if begin else "..." + value[-maxsize:]
    return value


def random_id():
    return uuid.uuid4()


def get_read_source_device(read_source):
    device_folder = str(Path(read_source.folder).parent)
    device = db_session.query(Device).filter_by(folder=device_folder).first()
    if not device:
        device = Device()
        device.folder = device_folder
        db_session.add(device)
        db_session.commit()
    return device

def delete_orphan_devices():
    devices = db_session.query(Device).all()
    for device in devices:
        if device.read_sources.count() == 0:
            db_session.delete(device)
    db_session.commit()