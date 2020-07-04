from models import *
from database import db_session
from helpers import get_config, get_page, get_chat_sources, clean_text, getErrorString
from renderizer.renderizer import Renderizer
import os
import pathlib
import settings
import shutil
import errno
from sinf.exe_finder import open_in_browser
from config_manager import config_manager
import constants
from sqlalchemy import or_
from report_maker.workers import chat_worker, general_images_worker, general_videos_worker, general_audios_worker, general_documents_worker
from multiprocessing import Pool, Process
from helpers_cmd import progress
from datetime import datetime


def make_filter(class_, query=None):
    if query is None:
        query = db_session.query(class_)
    if class_ == Message:
        query = query.filter(Message.checked, Message.chat.has(Chat.checked))
    else:
        query = query.filter(class_.checked)
    return query


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def add_chat_included(files):
    # filters = get_config("filters")
    for file_ in files:
        if file_.message_id is None:
            file_.message_id = False
            continue
        file_.message_id = file_.message.checked
    return files


class ReportBundle:
    def __init__(self):
        self.item_source_id = None
        self.item_source_type = None
        self.report_folder = None
        
    def filter(self, class_, query=None):
        query = make_filter(class_, query)
        if self.item_source_type == 'device':
            query = query.filter(class_.read_source.has(ReadSource.device_id == self.item_source_id))
        elif self.item_source_type == 'read_source':
            query = query.filter(class_.read_source_id == self.item_source_id)
        return query

class ReportMaker:
    def __init__(self):
        self.renderizer = None
      
    def set_item_source(self, item_source):
        self.report_bundle = ReportBundle()
        self.report_bundle.item_source_id = item_source.id
        self.report_bundle.item_source_type = "device" if isinstance(item_source, Device) else "read_source"
        self.report_bundle.report_folder = item_source.folder


    def copy_needed_files(self):
        folder = os.path.join(settings.app_dir, 'renderizer', 'html_files')
        dest_folder = os.path.join(self.report_bundle.report_folder, 'html_files')
        if not os.path.exists(dest_folder):
            shutil.copytree(folder, dest_folder)
        os.system("attrib +h " + dest_folder)


    def copy_file_create_dir(self, src, dest):
        try:
            shutil.copy(src, dest)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
            os.makedirs(os.path.dirname(dest))
            shutil.copy(src, dest)

    # def get_tags_with_hightlights(self):
    #     query = db_session.query(Tag).filter_by(highlight=True)
    #     if not self.device

    def render_chats(self):
        print("Renderizando chats")

        query = db_session.query(Chat.id)
        chats = self.report_bundle.filter(Chat, query).all()
        n = len(chats)
        pool = Pool(processes=config_manager.data['n_workers'])
        procs = ({'report_bundle': self.report_bundle, 'chat_id': item[0]} for item in chats)
        for i, _ in enumerate(pool.imap_unordered(chat_worker, procs)):
            progress(i, n)
        pool.close()
        pool.join()
        

    def render_contacts(self):
        print("Renderizando Contatos")
        contacts = self.report_bundle.filter(Contact).all()
        context = {'contacts': contacts}
        dest_file = os.path.join(
            self.report_bundle.report_folder, 'html_files', 'contacts.html')
        self.renderizer.render_template('contacts.html', dest_file,
                                        context)

    def render_smss(self):
        print("Renderizando SMS")
        smss = self.report_bundle.filter(Sms).all()
        context = {'smss': smss}
        dest_file = os.path.join(self.report_bundle.report_folder, 'html_files', 'smss.html')
        self.renderizer.render_template('smss.html', dest_file,
                                        context)

    def render_calls(self):
        print("Renderizando Chamadas")
        calls = self.report_bundle.filter(Call).all()
        context = {'calls': calls}
        dest_file = os.path.join(
            self.report_bundle.report_folder, 'html_files', 'calls.html')
        self.renderizer.render_template('calls.html', dest_file,
                                        context)


    def get_tags_highlight(self):
        if self.report_bundle.item_source_type == 'device':
            return db_session.query(Tag).filter(Tag.highlight == True, or_(Tag.messages.any(Message.read_source.has(ReadSource.device_id==self.report_bundle.item_source_id)),
                                                        Tag.smss.any(Sms.read_source.has(ReadSource.device_id==self.report_bundle.item_source_id)),
                                                        Tag.files.any(File.read_source.has(ReadSource.device_id==self.report_bundle.item_source_id)))).all()
        return db_session.query(Tag).filter(Tag.highlight == True, or_(Tag.messages.any(Message.read_source_id == self.report_bundle.item_source_id),
                                                        Tag.smss.any(Sms.read_source_id == self.report_bundle.item_source_id),
                                                        Tag.files.any(File.read_source_id == self.report_bundle.item_source_id))).all()

    def render_highlights(self):
        print("Renderizando páginas de destaque")
        tags_highlight = self.get_tags_highlight()

        for tag in tags_highlight:
            chat_messages = calls = smss = contacts = images = videos = audios = None
            query = db_session.query(Message).join(Chat).filter(
                Message.tags.any(Tag.id == tag.id)).order_by(Chat.id.asc(), Message.timestamp.asc())
            chat_messages = self.report_bundle.filter(Message, query).all()

            query = db_session.query(Call).filter(
                Call.tags.any(Tag.id == tag.id))
            calls = self.report_bundle.filter(Call, query).all()

            query = db_session.query(Sms).filter(Sms.tags.any(
                Tag.id == tag.id))
            smss = self.report_bundle.filter(Sms, query).all()

            query = db_session.query(Contact).filter(
                Contact.tags.any(Tag.id == tag.id))
            contacts = self.report_bundle.filter(Contact, query).all()

            query = db_session.query(File).filter(
                File.type_ == 'image', File.tags.any(Tag.id == tag.id))
            images = self.report_bundle.filter(File, query).all()

            query = db_session.query(File).filter(
                File.type_ == 'audio', File.tags.any(Tag.id == tag.id))
            audios = self.report_bundle.filter(File, query).all()

            query = db_session.query(File).filter(
                File.type_ == 'video', File.tags.any(Tag.id == tag.id))
            videos = self.report_bundle.filter(File, query).all()


            context = {'chat_messages': chat_messages, 'calls': calls, 'smss': smss,
                       'contacts': contacts, 'images': images, 'videos': videos,
                       'audios': audios, 'title': tag.name, 'description': tag.description}
            dest_file = os.path.join(
                self.report_bundle.report_folder, 'html_files', "highlights_{}.html".format(clean_text(tag.name)))

            self.renderizer.render_template('highlights.html', dest_file,
                                            context)

    def render_main_page(self, items_available):
        print("Renderizando página principal")
        calls = db_session.query(Call).all()
        tags_highlight = self.get_tags_highlight()
        context = {'report_config': config_manager.report_config,
                   'sources': get_chat_sources(self.report_bundle.filter(Chat)),
                   'tags_highlight': tags_highlight,
                   'items_available': items_available}
        dest_file = os.path.join(self.report_bundle.report_folder, constants.HTML_REPORT_NAME)
        self.renderizer.render_template('main.html', dest_file,
                                        context)

    def render_home_page(self):
        print("Renderizando home page")
        context = {}
        dest_file = os.path.join(self.report_bundle.report_folder, "html_files", "home.html")
        self.renderizer.render_template('home.html', dest_file,
                                        context)

    def get_items_available(self):
        items = []
        if self.report_bundle.filter(Chat).count() > 0:
            items.append("chat")
        if self.report_bundle.filter(Sms).count() > 0:
            items.append("sms")
        if self.report_bundle.filter(Contact).count() > 0:
            items.append("contact")
        if self.report_bundle.filter(Call).count() > 0:
            items.append("call")
        query = db_session.query(File).filter(File.type_ == 'image')
        query = self.report_bundle.filter(File, query)
        if query.count() > 0:
            items.append("image")
        query = db_session.query(File).filter(File.type_ == 'audio')
        query = self.report_bundle.filter(File, query)
        if query.count() > 0:
            items.append("audio")
        query = db_session.query(File).filter(File.type_ == 'video')
        query = self.report_bundle.filter(File, query)
        if query.count() > 0:
            items.append("video")
        query = db_session.query(File).filter(~File.type_.in_(['video', 'audio', 'image']))
        query = self.report_bundle.filter(File, query)
        if query.count() > 0:
            items.append("document")
        return items

    def generate_html_files(self):
        start_time = datetime.now()
        self.renderizer = Renderizer(self.report_bundle.report_folder)
        # self.copy_files()
        self.copy_needed_files()
        print("Renderizando arquivos HTML...")
        old_unknow_avatar = settings.unknow_avatar
        settings.unknow_avatar = "assets\\desconhecido.html"
        items_available = self.get_items_available()
        if 'chat' in items_available:
            self.render_chats()
        if 'call' in items_available:
            self.render_calls()
        if 'sms' in items_available:
            self.render_smss()
        if 'contact' in items_available:
            self.render_contacts()
        processes = []
        data = {'report_bundle': self.report_bundle}
        if 'image' in items_available:
            p = Process(target=general_images_worker, args=(data,))
            p.start()
            processes.append(p)
        if 'video' in items_available:
            p = Process(target=general_videos_worker, args=(data,))
            p.start()
            processes.append(p)
        if 'audio' in items_available:
            p = Process(target=general_audios_worker, args=(data,))
            p.start()
            processes.append(p)
        if 'document' in items_available:
            p = Process(target=general_documents_worker, args=(data,))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        self.render_highlights()
        self.render_home_page()
        self.render_main_page(items_available)
        settings.unknow_avatar = old_unknow_avatar

        delta = datetime.now() - start_time
        print(f"\nProcessamento finalizado. Tempo gasto: {delta}")

    def open_chats(self):
        files = os.listdir(self.report_bundle.report_folder)
        for file_ in files:
            if file_.endswith(".html"):
                open_in_browser(os.path.join(
                    self.report_bundle.report_folder, file_), file_path=True)
                # command = "start {}".format(open_file)
                # os.system(command)


if __name__ == "__main__":
    import sys

    # os.system("color 1f")
    report_maker = ReportMaker()
    report_maker.generate_html_files()
    report_maker.open_chats()
