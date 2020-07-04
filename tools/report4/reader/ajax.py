from flask import Blueprint, request, session, jsonify, render_template, send_from_directory, send_file, flash
from models import *
from helpers_models import *
from helpers_http import *
import queries as queries
from forms import *
import settings
import urllib.request
import subprocess
# import win32api
import ctypes
import shutil
from report_docx.report_maker import ReportMaker
import inflection

ajax = Blueprint('ajax', __name__)


@ajax.route("/workdir/<path:relative_path>")
def workdir(relative_path):
    relative_path = urllib.request.url2pathname(relative_path)
    absolute_path = settings.work_dir / relative_path
    return send_from_directory(os.path.dirname(absolute_path), os.path.basename(absolute_path), as_attachment=False)


@ajax.route("/set-current-tag")
def set_current_tag():
    id = request.args.get('id', type=int)
    tag = db_session.query(Tag).get(id)
    if tag:
        session['current_tag_id'] = tag.id
        return 'ok'
    return 'error', 404


# @ajax.route("/filters-post", methods=['POST'])
# def filters_post():
#     filters = json.loads(request.form['filters'])
#     for dev in filters['devices']:
#         device = db_session.query(Device).get(dev['id'])
#         if device:
#             device.checked = dev['checked']
#             db_session.add(device)
#     db_session.commit()
#     set_config('filters', {
#         'tag': filters['tag'],
#         'checked': filters['checked']
#     })
#     return 'ok'


@ajax.route("/toggle-one-tag")
def toggle_one_tag():
    classname = request.args.get('classname')
    obj_id = request.args.get('obj_id', type=int)
    tag = db_session.query(Tag).get(session['current_tag_id'])
    if tag:
        obj = db_session.query(globals()[classname]).get(obj_id)
        if tag in obj.tags:
            toggle = 'remove'
            obj.tags.remove(tag)
        else:
            toggle = 'append'
            obj.tags.append(tag)
        db_session.add(obj)
        db_session.commit()
        return jsonify({'tag_name': tag.name, 'tag_color': tag.color, 'toggle': toggle, 'tag_id': tag.id})
    return 'error', 404


@ajax.route("/add-many-tags", methods=['POST'])
def add_many_tags():
    tag = db_session.query(Tag).get(session['current_tag_id'])
    if tag:
        classname = request.form['classname']
        item_ids = json.loads(request.form['item_ids'])
        class_ = globals()[classname]
        objs = db_session.query(class_).filter(class_.id.in_(item_ids)).all()
        for obj in objs:
            if not tag in obj.tags:
                obj.tags.append(tag)
                db_session.add(obj)
        db_session.commit()
        return jsonify({'tag_name': tag.name, 'tag_color': tag.color, 'tag_id': tag.id})
    return 'error', 404


@ajax.route("/remove-many-tags", methods=['POST'])
def remove_many_tags():
    tag = db_session.query(Tag).get(session['current_tag_id'])
    if tag:
        classname = request.form['classname']
        item_ids = json.loads(request.form['item_ids'])
        class_ = globals()[classname]
        objs = db_session.query(class_).filter(class_.id.in_(item_ids)).all()
        for obj in objs:
            if tag in obj.tags:
                obj.tags.remove(tag)
                db_session.add(obj)
        db_session.commit()
        return jsonify({'tag_name': tag.name, 'tag_color': tag.color, 'tag_id': tag.id})
    return 'error', 404


@ajax.route("/add-many-tags-complete", methods=['POST'])
def add_many_tags_complete():
    tag = db_session.query(Tag).get(session['current_tag_id'])
    if tag:
        classname = request.args.get('classname')
        class_ = globals()[classname]
        form = globals()[f"{classname}Form"](request.form)
        query = make_filter(class_)
        query = queries.class_dict[classname](query, form)
        query = query.filter(~class_.tags.any(Tag.id == tag.id))
        for obj in query.all():
            obj.tags.append(tag)
            db_session.add(obj)
        db_session.commit()
        return jsonify({'tag_name': tag.name, 'tag_color': tag.color, 'tag_id': tag.id})
    return 'error', 404


@ajax.route("/remove-many-tags-complete", methods=['POST'])
def remove_many_tags_complete():
    tag = db_session.query(Tag).get(session['current_tag_id'])
    if tag:
        classname = request.args.get('classname')
        class_ = globals()[classname]
        form = globals()[f"{classname}Form"](request.form)
        query = make_filter(class_)
        query = queries.class_dict[classname](query, form)
        query = query.filter(class_.tags.any(Tag.id == tag.id))
        for obj in query.all():
            obj.tags.remove(tag)
            db_session.add(obj)
        db_session.commit()
        return jsonify({'tag_name': tag.name, 'tag_color': tag.color, 'tag_id': tag.id})
    return 'error', 404


@ajax.route("/check-item")
def check_item():
    item_id = request.args.get('id', type=int)
    class_name = request.args.get('class', type=str)
    obj = db_session.query(globals()[class_name]).get(item_id)
    if obj:
        obj.checked = True
        db_session.add(obj)
        db_session.commit()
        return f'{class_name} {item_id} checked'
    return 'error', 404


@ajax.route("/uncheck-item")
def uncheck_item():
    item_id = request.args.get('id', type=int)
    class_name = request.args.get('class', type=str)
    obj = db_session.query(globals()[class_name]).get(item_id)
    if obj:
        obj.checked = False
        db_session.add(obj)
        db_session.commit()
        return f'{class_name} {item_id} unchecked'
    return 'error', 404


# @ajax.route("/remove-tag-all-page", methods=['POST'])
# def remove_tag_all_page():
#     item_ids = json.loads(request.form['ids'])
#     class_name = request.form['class']
#     tag = db_session.query(Tag).get(session['current_tag_id'])
#     for item_id in item_ids:
#         obj = db_session.query(globals()[class_name]).get(item_id)
#         if obj and tag and tag in obj.tags:
#             obj.tags.remove(tag)
#             db_session.add(obj)
#     db_session.commit()
#     return 'ok'


@ajax.route("/check_all", methods=['POST'])
def check_all():
    item_ids = json.loads(request.form['ids'])
    class_name = request.form['class']
    for item_id in item_ids:
        obj = db_session.query(globals()[class_name]).get(item_id)
        if obj:
            obj.checked = True
            db_session.add(obj)
    db_session.commit()
    return 'ok'


@ajax.route("/uncheck-all", methods=['POST'])
def uncheck_all():
    item_ids = json.loads(request.form['ids'])
    class_name = request.form['class']
    for item_id in item_ids:
        obj = db_session.query(globals()[class_name]).get(item_id)
        if obj:
            obj.checked = False
            db_session.add(obj)
    db_session.commit()
    return 'ok'


@ajax.route("/check-all-complete", methods=['POST'])
def check_all_complete():
    classname = request.args.get('classname')
    class_ = globals()[classname]
    form = globals()[f"{classname}Form"](request.form)
    query = make_filter(class_)
    query = queries.class_dict[classname](query, form)
    for obj in query.all():
        obj.checked = True
        db_session.add(obj)
    db_session.commit()
    return 'ok'


@ajax.route("/uncheck-all-complete", methods=['POST'])
def uncheck_all_complete():
    classname = request.args.get('classname')
    class_ = globals()[classname]
    form = globals()[f"{classname}Form"](request.form)
    query = make_filter(class_)
    query = queries.class_dict[classname](query, form)
    for obj in query.all():
        obj.checked = False
        db_session.add(obj)
    db_session.commit()
    return 'ok'


@ajax.route("/tag")
def tag():
    tag = db_session.query(Tag).get(request.args.get('id', type=int))
    if tag:
        schema = TagSchema()
        return jsonify({
            'id': tag.id,
            'name': tag.name,
            'description': tag.description,
            'highlight': tag.highlight,
            'color': tag.color
        })
    return 'error', 404


@ajax.route("/toggle-navbar")
def toggle_navbar():
    try:
        value = request.args.get('active')
        session['navbar_active'] = value
        return 'ok'
    except:
        return 'error', 404


@ajax.route("/set-file-vizualization")
def set_file_vizualization():
    mode = request.args.get('mode')
    session['file_vizualization'] = mode
    return 'ok'


@ajax.route("/open-file/<int:id>")
def open_file(id):
    obj = db_session.query(File).get(id)
    if obj:
        path = settings.work_dir / obj.path
        if os.path.exists(path):
            # win32api.ShellExecute(0, None, str(path), None, None, 0)
            ctypes.windll.shell32.ShellExecuteW(
                0, None, str(path), None, None, 0)
        return 'ok'
    return 'error', 404


@ajax.route("/open-file-with/<int:id>")
def open_file_with(id):
    obj = db_session.query(File).get(id)
    if obj:
        path = settings.work_dir / obj.path
        if os.path.exists(path):
            # win32api.ShellExecute(0, None, "openwith", f"\"{str(path)}\"", None, 0)
            ctypes.windll.shell32.ShellExecuteW(
                0, None, u'openwith.exe', f"\"{str(path)}\"", None, 0)
        return 'ok'
    return 'error', 404


@ajax.route("/show-in-folder/<int:id>")
def see_in_folder(id):
    print(id)
    obj = db_session.query(File).get(id)
    if obj:
        path = settings.work_dir / obj.path
        if os.path.exists(path):
            ctypes.windll.shell32.ShellExecuteW(
                None, u'open', u'explorer.exe', u'/n,/select, ' + f"\"{str(path)}\"", None, 1)
        return 'ok'
    return 'error', 404


@ajax.route("/get-page-message")
def get_page_message():
    id = request.args.get('id', type=int)
    message = db_session.query(Message).get(id)
    message_ids = make_filter(Message, db_session.query(Message.id).filter_by(chat_id=message.chat_id)).order_by(
        Message.timestamp.asc()).all()
    pos = None
    for i, j in enumerate(message_ids):
        if j == (message.id,):
            pos = i
            break
    page = int(pos / settings.per_page['chat']) + 1
    return jsonify({'chat_id': message.chat_id, 'page': page})


@ajax.route("/new-tag")
def new_tag():
    tag = Tag()
    return render_template("ajax/new-tag.html", tag=tag)


@ajax.route("/tags-post", methods=['POST'])
def tags_post():
    tags_data = json.loads(request.form['tags'])
    tag_ids = []
    for tag_data in tags_data:
        try:
            tag_id = int(tag_data['id'])
        except ValueError:
            tag_id = None
        tag = db_session.query(Tag).get(tag_id) if tag_id else None
        if not tag:
            tag = Tag()
            db_session.add(tag)
            db_session.commit()
        tag.name = tag_data['name']
        tag.description = tag_data['description']
        tag.highlight = tag_data['highlight']
        tag.color = tag_data['color']
        db_session.add(tag)
        tag_ids.append(tag.id)
    db_session.commit()
    tags_delete = db_session.query(Tag).filter(~Tag.id.in_(tag_ids)).all()
    for t in tags_delete:
        db_session.delete(t)
    db_session.commit()
    return 'ok'


@ajax.route("/check-folder-existence")
def check_folder_existence():
    path = Path(request.args.get('path'))
    if path.exists() and path.is_dir():
        return 'true'
    return 'false'


@ajax.route("/export-files", methods=['POST'])
def export_files():
    directory = Path(request.args.get('directory'))
    form = FileForm(request.form)
    query = queries.files(File.query, form)
    query = make_filter(File, query)
    files = query.all()
    try:
        for file in files:
            path = settings.work_dir / file.path
            path_to = directory / path.name
            i = 1
            print(path_to)
            while path_to.exists():
                path_to = directory / f"{path.name}_{i}"
                i += 1
            shutil.copy2(path, path_to)
        return 'ok'
    except Exception as e:
        print(e)
        return str(e), 404


@ajax.route("/images-docx", methods=['POST'])
def images_docx():
    type_ = request.args.get('type')
    form = FileForm(request.form)
    query = queries.files(File.query, form)
    query = make_filter(File, query)
    try:
        rm = ReportMaker()
        query = query.filter(File.type_ == 'image') if type_ == 'image' else query.filter(File.type_ == 'video',
                                                                                          File.analise_thumb != None)
        path = rm.make_images(query, n_cols=3)
        if path and path.exists():
            return send_file(str(path))
    except Exception as e:
        print(e)
        pass
    flash("Não foi possível gerar o docx com as imagens", "alert-danger")
    return render_template('erro.html')


@ajax.route("/chat-docx-individual", methods=['POST'])
def chat_docx_individual():
    form = MessageForm(request.form)
    query = queries.messages(Message.query, form)
    query = make_filter(Message, query)
    try:
        rm = ReportMaker()
        path = rm.make_chat(query)
        if path and path.exists():
            return send_file(str(path))
    except Exception as e:
        print(e)
    flash("Não foi possível gerar o docx com as imagens", "alert-danger")
    return render_template('erro.html')


@ajax.route("/chat-docx-complete", methods=['POST'])
def chat_docx_complete():
    directory = Path(request.args.get('directory'))
    form = MessageForm(request.form)
    query = db_session.query(queries.messages(Message).join(Chat), form)
    query = make_filter(Message, query)
    chats = [message.chat for message in query.distinct(Message.chat_id)]
    print(len(chats))
    try:
        for chat in chats:
            print(chat.friendly_identifier)
            path = directory / f"{inflection.camelize(chat.friendly_identifier)}.docx"
            rm = ReportMaker()
            path = rm.make_chat(query.filter(Message.chat == chat), path=path, chat=chat)
    except Exception as e:
        print(e)
    flash("Não foi possível gerar o docx com as imagens", "alert-danger")
    return render_template('erro.html')




# @ajax.route("/video-thumbs-docx", methods=['POST'])
# def video_thumbs_docx():
#     form = FileForm(request.form)
#     query = queries.files(File.query, form)
#     query = make_filter(File, query)
#     query = query.filter(File.type_ == 'video', File.analise_thumb != None)
#     rm = ReportMaker()
#     path = rm.make_images(query, n_cols=3)
#     if path.exists():
#         return send_file(str(path))

#     return 'error', 404
