from flask import Blueprint, render_template, session, request, redirect
from models import *
from database import db_session
from helpers_http import *
from helpers_models import *
import settings
import queries as queries
import json
from forms import *

views = Blueprint('views', __name__)


@views.route("/")
def index():
    # tag = db_session.query(Tag).filter_by(highlight = True).first()
    # if tag:
    #     return redirect(url_for('views.highlights', tag_id=tag.id))
    return redirect(url_for('views.tutoriais'))


@views.route("/tutoriais")
def tutoriais():
    folder = Path(settings.app_dir / "static/tutorial_videos/geral")
    files_general = folder.iterdir()
    if settings.exec_mode != 'portable':
        folder = Path(settings.app_dir / "static/tutorial_videos/peritos")
        files_peritos = folder.iterdir()
    else:
        files_peritos = None
    return render_template(f"tutorial/home.html", files_general=files_general, files_peritos=files_peritos)


@views.route("/chat-list/<int:page>", methods=['GET', 'POST'])
def chat_list(page):
    form = ChatForm(request.form)
    query = make_filter(Chat)
    if form.validate_on_submit() or request.method == 'GET':
        query = queries.chat_list(query, form)
    pagination = get_page(query, settings.per_page['chat'], page=page)
    return render_template("chat_list.html", pagination=pagination, form=form)


@views.route("/tags")
def tags():
    tags = db_session.query(Tag).all()
    return render_template("tags.html", tags=tags)


@views.route("/tag-post", methods=["POST"])
def tag_post():
    id = request.form['id']
    if id:
        tag = db_session.query(Tag).get(id)
    else:
        tag = Tag()
    tag.name = request.form["name"]
    tag.color = request.form["color"]
    tag.description = request.form['description']
    tag.highlight = True if 'highlight' in request.form.keys() else False
    db_session.add(tag)
    db_session.commit()
    return redirect(url_for("views.tags"))


# @views.route("/files/<type_>/<int:page>")
# def files(page, type_=None):
#     form = FileForm(request.form)
#     form.type_ == type_
#     query = make_filter(File)
#     pagination = get_page(query, per_page=settings.per_page[type_], page=page)
#     return render_template('files-details.html', pagination=pagination, title="Arquivos", args={}, view='views.files_post', form=form)


@views.route("/files/<int:page>", methods=['GET', 'POST'])
def files(page):
    query = make_filter(File)
    form = FileForm(request.form)
    if request.method == 'POST' and form.validate():
        query = queries.files(query, form)
    per_page = settings.per_page[form.type_.data] if form.type_.data != 'all' else settings.per_page['file']
    pagination = get_page(query, per_page=per_page, page=page)
    try:
        template = 'files-table.html' if session['file_vizualization'] == 'table' else 'files-mini.html'
    except KeyError:
        session['file_vizualization'] = 'table'
        template = 'files-table.html'
    return render_template(template, pagination=pagination, args={}, view='views.files', form=form)


@views.route("/chat/<int:page>", methods=['GET', 'POST'])
def chat(page):
    form = MessageForm(request.form)
    query = make_filter(Message, db_session.query(Message).join(Chat))
    if request.method == 'POST' and form.validate():
        query = queries.messages(query, form)
        chat = db_session.query(Chat).get(form.chat_id.data) if form.chat_id.data else None
    else:
        chat_id = request.args.get('chat_id', type=int)
        if chat_id:
            chat = db_session.query(Chat).get(chat_id)
            query = query.filter(Message.chat_id == chat_id).order_by(Message.timestamp.asc())
            form.chat_id.data = chat_id
        else:
            chat = None
            db_session.query(Message).order_by(Message.timestamp.asc())

    pagination = get_page(query, per_page=settings.per_page['chat'], page=page)
    return render_template("chat.html", chat=chat, pagination=pagination, view='views.chat', args={}, form=form)


@views.route("/smss/<int:page>", methods=['GET', 'POST'])
def smss(page):
    form = SmsForm(request.form)
    query = make_filter(Sms)
    if request.method == 'POST' and form.validate():
        query = queries.smss(query, form)
    else:
        query = query.order_by(Sms.timestamp.asc())
    pagination = get_page(query, per_page=settings.per_page['sms'], page=page)
    return render_template("smss.html", pagination=pagination, view='views.smss', form=form)


@views.route("/contacts/<int:page>", methods=['GET', 'POST'])
def contacts(page):
    form = ContactForm(request.form)
    query = make_filter(Contact)
    if request.method == 'POST' and form.validate():
        query = queries.contacts(query, form)
    else:
        query = query.order_by(Contact.name.asc())
    pagination = get_page(query, per_page=settings.per_page['contact'], page=page)
    return render_template("contacts.html", pagination=pagination, view='views.contacts', form=form)


@views.route("/calls/<int:page>", methods=['GET', 'POST'])
def calls(page):
    form = CallForm(request.form)
    query = make_filter(Call)
    if request.method == 'POST' and form.validate():
        query = queries.calls(query, form)
    else:
        query = query.order_by(Call.timestamp.asc())
    pagination = get_page(query, per_page=settings.per_page['call'], page=page)
    return render_template("calls.html", pagination=pagination, view='views.calls', form=form)


@views.route("/highlights/<int:tag_id>")
def highlights(tag_id):
    tag = db_session.query(Tag).get(tag_id)
    smss = db_session.query(Sms).filter(Sms.tags.any(Tag.id == tag.id)).order_by(Sms.timestamp.asc()).all()
    messages = db_session.query(Message).join(Chat).filter(Message.tags.any(Tag.id == tag.id)).order_by(Chat.id.asc(),
                                                                                            Message.timestamp.asc()).all()
    files = db_session.query(File).filter(File.tags.any(Tag.id == tag.id)).order_by(File.type_.asc()).all()
    return render_template('highlights.html', tag=tag, smss=smss, messages=messages, files=files)


@views.route("/filters")
def filters():
    filters = get_user_filters()
    tags = db_session.query(Tag).all()
    devices = db_session.query(Device).order_by(Device.folder.asc()).all()
    devices_ = [{'id': dev.id, 'folder': dev.folder, 'checked': dev.id not in filters['devices']} for dev in devices]
    tags_ = [{'id': tag.id, 'name': tag.name, 'checked': tag.id in filters['tags']} for tag in tags]
    data = {'devices': devices_, 'tags': tags_}
    return render_template("filters2.html", data=data)

@views.route("/filters", methods=['POST'])
def filters_post():
    payload = get_json_payload(request)
    set_user_filters(payload)
    return redirect(url_for('views.filters'))
