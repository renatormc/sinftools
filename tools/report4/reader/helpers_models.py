from models import *
from database import db_session
from sqlalchemy import or_
import settings
from pathlib import Path
from flask import session

def unique_join(query, *props, **kwargs):
    if props[0] in [c.entity for c in query._join_entities]:
        return query
    return query.join(*props, **kwargs)

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


def get_config(key):
    config = db_session.query(Config).filter_by(key=key).first()
    if config:
        return config.get_value()


def set_config(key, value):
    config = db_session.query(Config).filter_by(key=key).first()
    if not config:
        config = Config()
        config.key = key
    config.set_value(value)
    db_session.add(config)
    db_session.commit()


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def get_page(query, per_page, page=1, only_count=False, gen_links=True):
    qtd = query.count()
    total = int(qtd / per_page)
    if qtd % per_page != 0:
        total += 1
    if only_count:
        return total
    if page > total and total > 0:
        page = total
    first_element = (page - 1) * per_page
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
                      "active": False, 'disabled': disabled, 'class': 'rm-page-link'})
        links.append({'page': page - 1, "html": "<",
                      "active": False, 'disabled': disabled, 'class': 'rm-page-link rm-page-previous'})
        for i in range(first, last + 1):
            active = i == page
            links.append(
                {'page': i, "html": i, "active": active, 'disabled': False, 'class': 'rm-page-link'})
        disabled = True if page == last else False
        links.append({'page': page + 1, "html": ">",
                      "active": False, 'disabled': disabled, 'class': 'rm-page-link rm-page-next'})
        links.append({'page': total, "html": ">>",
                      "active": False, 'disabled': disabled, 'class': 'rm-page-link'})

    return {
        "n_items": qtd,
        "first": (page - 1)*per_page,
        "items": items,
        "page": page,
        "pages": total,
        "per_page": per_page,
        'links': links
    }


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


def make_filter(class_, query=None, exclude_checked=False):
    filters = get_user_filters()
    if query is None:
        query = db_session.query(class_)
    query = query.join(ReadSource).join(Device)
    if filters:
        if filters['tags']:
            if class_ == Chat:
                query = query.filter(or_(Chat.messages.any(Message.tags.any(Tag.id.in_(filters['tags']))), class_.tags.any(Tag.id.in_(filters['tags']))))
            else:
                query = query.filter(class_.tags.any(Tag.id.in_(filters['tags'])))
        if filters['devices']:
            query = query.filter(~Device.id.in_(filters['devices']))
        # if filters['checked'] is not None or exclude_checked:
        #     query = query.filter(class_.checked == filters['checked'])
        #     if class_ == Message:
        #         query = query.filter(Message.chat.has(Chat.checked == filters['checked']))
    return query



def get_user_filters():
    try:
        return json.loads(session['filters'])
    except KeyError:
        set_user_filters({'devices': [], 'tags': []})
        return json.loads(session['filters'])


def set_user_filters(filters):
    
    key = f"filter"
    set_config(key, filters)
    session['filters'] = json.dumps(filters)


def get_chat_proprietary(read_source, app):
    return db_session.query(Participant).filter(Participant.read_source == read_source, Chat.source == app, Participant.proprietary).first()
