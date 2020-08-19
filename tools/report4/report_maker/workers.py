from config_manager import config_manager
from models import *
from database import db_connect
from renderizer.renderizer import Renderizer
from helpers import get_page, get_chat_sources


def add_chat_included(files):
    # filters = get_config("filters")
    for file_ in files:
        if file_.message_id is None:
            file_.chat_included = False
            continue
        file_.chat_included = file_.message.checked
    return files


class GeneralImagesWorker:

    def __init__(self, report_bundle):
        self.report_bundle = report_bundle
        self.renderizer = Renderizer(self.report_bundle.report_folder)


    def run(self):
        try:
            self.engine, self.dbsession = db_connect()
            print("Renderizando imagens gerais")
            query = self.dbsession.query(File).filter(File.type_ == 'image')
            query = self.report_bundle.filter(File, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['image'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['image'])
                # Adiciona informação nos anexos se o chat foi incluido ou não
                add_chat_included(pagination['items'])
                context = {'pagination': pagination}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"general-images_page_{page}.html")
                self.renderizer.render_template('general-images.html', dest_file,
                                                context)
        finally:
            self.engine.dispose()


def general_images_worker(data):
    worker = GeneralImagesWorker(report_bundle=data['report_bundle'])
    worker.run()


class GeneralVideosWorker:

    def __init__(self, report_bundle):
        self.report_bundle = report_bundle
        self.renderizer = Renderizer(self.report_bundle.report_folder)
      

    def run(self):
        try:
            self.engine, self.dbsession = db_connect()
            print("Renderizando videos gerais")
            query = self.dbsession.query(File).filter(File.type_ == 'video')
            query = self.report_bundle.filter(File, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['video'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['video'])
                # Adiciona informação nos anexos se o chat foi incluido ou não
                add_chat_included(pagination['items'])
                context = {'pagination': pagination}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"general-videos_page_{page}.html")
                self.renderizer.render_template('general-videos.html', dest_file,
                                                context)
        finally:
            self.engine.dispose()


def general_videos_worker(data):
    worker = GeneralVideosWorker(report_bundle=data['report_bundle'])
    worker.run()


class GeneralAudiosWorker:

    def __init__(self, report_bundle):
        self.report_bundle = report_bundle
        self.renderizer = Renderizer(self.report_bundle.report_folder)


    def run(self):
        try:
            self.engine, self.dbsession = db_connect()
            print("Renderizando audios gerais")
            query = self.dbsession.query(File).filter(File.type_ == 'audio')
            query = self.report_bundle.filter(File, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['audio'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['audio'])
                # Adiciona informação nos anexos se o chat foi incluido ou não
                add_chat_included(pagination['items'])
                context = {'pagination': pagination}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"general-audios_page_{page}.html")
                self.renderizer.render_template('general-audios.html', dest_file,
                                                context)
        finally:
            self.engine.dispose()


def general_audios_worker(data):
    worker = GeneralAudiosWorker(report_bundle=data['report_bundle'])
    worker.run()


class GeneralDocumentsWorker:

    def __init__(self, report_bundle):
        self.report_bundle = report_bundle
        self.renderizer = Renderizer(self.report_bundle.report_folder)



    def run(self):
        try:
            self.engine, self.dbsession = db_connect()
            print("Renderizando documents gerais")
            query = self.dbsession.query(File).filter(~File.type_.in_(['video', 'audio', 'image']))
            query = self.report_bundle.filter(File, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['document'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['document'])
                # Adiciona informação nos anexos se o chat foi incluido ou não
                add_chat_included(pagination['items'])
                context = {'pagination': pagination}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"general-documents_page_{page}.html")
                self.renderizer.render_template('general-documents.html', dest_file,
                                                context)
        finally:
            self.engine.dispose()


def general_documents_worker(data):
    worker = GeneralDocumentsWorker(report_bundle=data['report_bundle'])
    worker.run()


class ChatWorker:

    def __init__(self, report_bundle):
        self.report_bundle = report_bundle
        self.renderizer = Renderizer(self.report_bundle.report_folder)



    def run(self, chat_id):
        self.engine, self.dbsession = db_connect()

        chat = self.dbsession.query(Chat).get(chat_id)
        print(
            f"Renderizando chat {chat.friendly_identifier} ({chat.source})")
        query = self.dbsession.query(Message).filter(
            Message.analise_attachment_types.like("%image%"), Message.chat == chat)
        total_images = self.report_bundle.filter(Message, query).count()
        query = self.dbsession.query(Message).filter(
            Message.analise_attachment_types.like("%audio%"), Message.chat == chat)
        total_audios = self.report_bundle.filter(Message, query).count()
        query = self.dbsession.query(Message).filter(
            Message.analise_attachment_types.like("%video%"), Message.chat == chat)
        total_videos = self.report_bundle.filter(Message, query).count()
        query = self.dbsession.query(Message).filter_by(
            chat_id=chat.id).order_by(Message.timestamp.asc())

        query = self.report_bundle.filter(Message, query)
        n_pages = get_page(query, only_count=True,
                           per_page=config_manager.report_config['per_page']['chat'])
        for i in range(n_pages):
            page = i + 1
            pagination = get_page(
                query, page=page, per_page=config_manager.report_config['per_page']['chat'])
            context = {"pagination": pagination, 'chat': chat, 'total_images': total_images,
                       'total_videos': total_videos, 'total_audios': total_audios}
            dest_file = os.path.join(
                self.report_bundle.report_folder, 'html_files', f"chat{chat.id}_page_{page}.html")
            self.renderizer.render_template('chat.html', dest_file,
                                            context)
            for message in pagination['items']:
                message.page_renderized = page
                self.dbsession.add(message)
        self.dbsession.commit()

        # Audio pages
        query = self.dbsession.query(Message).filter(
            Message.analise_attachment_types.like("%audio%"), Message.chat == chat)
        query = self.report_bundle.filter(Message, query)
        n_pages = get_page(query, only_count=True,
                           per_page=config_manager.report_config['per_page']['audio'])
        for i in range(n_pages):
            page = i + 1
            pagination = get_page(
                query, page=page, per_page=config_manager.report_config['per_page']['audio'])
            context = {'pagination': pagination, 'chat': chat}
            dest_file = os.path.join(
                self.report_bundle.report_folder, 'html_files', f"audios{chat.id}_page_{page}.html")
            self.renderizer.render_template('audios.html', dest_file,
                                            context)

        # Image pages
        query = self.dbsession.query(Message).filter(
            Message.analise_attachment_types.like("%image%"), Message.chat == chat)
        query = self.report_bundle.filter(Message, query)
        n_pages = get_page(query, only_count=True,
                           per_page=config_manager.report_config['per_page']['image'])
        for i in range(n_pages):
            page = i + 1
            pagination = get_page(
                query, page=page, per_page=config_manager.report_config['per_page']['image'])
            context = {'pagination': pagination, 'chat': chat}
            dest_file = os.path.join(
                self.report_bundle.report_folder, 'html_files', f"images{chat.id}_page_{page}.html")
            self.renderizer.render_template('images.html', dest_file,
                                            context)

        # Video pages
        query = self.dbsession.query(Message).filter(
            Message.analise_attachment_types.like("%video%"), Message.chat == chat)
        query = self.report_bundle.filter(Message, query)
        n_pages = get_page(query, only_count=True,
                           per_page=config_manager.report_config['per_page']['video'])
        for i in range(n_pages):
            page = i + 1
            pagination = get_page(
                query, page=page, per_page=config_manager.report_config['per_page']['video'])
            context = {'pagination': pagination, 'chat': chat}
            dest_file = os.path.join(
                self.report_bundle.report_folder, 'html_files', f"videos{chat.id}_page_{page}.html")
            self.renderizer.render_template('videos.html', dest_file,
                                            context)

        # Participants
        context = {'participants': chat.participants, 'chat': chat}
        dest_file = os.path.join(
            self.report_bundle.report_folder, 'html_files', f"participants{chat.id}.html")
        self.renderizer.render_template('participants.html', dest_file,
                                        context)

        sources = get_chat_sources(self.report_bundle.filter(Chat))
        for source in sources:
            print(
                f"Renderizando todos os áudios de bate-papo do aplicativo {source}")
            # All Audios
            query = self.dbsession.query(Message).join(Chat).filter(Message.analise_attachment_types.like("%audio%"),
                                                                    Chat.source == source)
            query = self.report_bundle.filter(Message, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['audio'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['audio'])
                context = {'pagination': pagination, 'source': source}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"all-audios{source}_page_{page}.html")
                self.renderizer.render_template('all-audios.html', dest_file,
                                                context)

            # All Images
            print(
                f"Renderizando todas as imagens de bate-papo do aplicativo {source}")
            query = self.dbsession.query(Message).join(Chat).filter(Message.analise_attachment_types.like("%image%"),
                                                                    Chat.source == source)
            query = self.report_bundle.filter(Message, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['image'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['image'])
                context = {'pagination': pagination, 'source': source}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"all-images{source}_page_{page}.html")
                self.renderizer.render_template('all-images.html', dest_file,
                                                context)

            # All Videos
            print(
                f"Renderizando todos os videos de bate-papo do aplicativo {source}")
            query = self.dbsession.query(Message).join(Chat).filter(Message.analise_attachment_types.like("%video%"),
                                                                    Chat.source == source)
            query = self.report_bundle.filter(Message, query)
            n_pages = get_page(query, only_count=True,
                               per_page=config_manager.report_config['per_page']['video'])
            for i in range(n_pages):
                page = i + 1
                pagination = get_page(
                    query, page=page, per_page=config_manager.report_config['per_page']['video'])
                context = {'pagination': pagination, 'source': source}
                dest_file = os.path.join(
                    self.report_bundle.report_folder, 'html_files', f"all-videos{source}_page_{page}.html")
                self.renderizer.render_template('all-videos.html', dest_file,
                                                context)

            context = {}
            query = self.report_bundle.filter(Chat, self.dbsession.query(
                Chat).filter(Chat.source == source)).order_by(Chat.last_activity.desc())
            context['chats'] = query.all()
            query = self.dbsession.query(Message).join(Chat).filter(Message.analise_attachment_types.like("%audio%"),
                                                                    Chat.source == source)
            query = self.report_bundle.filter(Message, query)
            context['total_audios'] = query.count()
            query = self.dbsession.query(Message).join(Chat).filter(Message.analise_attachment_types.like("%video%"),
                                                                    Chat.source == source)
            query = self.report_bundle.filter(Message, query)
            context['total_videos'] = query.count()
            query = self.dbsession.query(Message).join(Chat).filter(Message.analise_attachment_types.like("%image%"),
                                                                    Chat.source == source)
            query = self.report_bundle.filter(Message, query)
            context['total_images'] = query.count()
            context['source'] = source
            dest_file = os.path.join(
                self.report_bundle.report_folder, 'html_files', f"chats_{source}.html")
            self.renderizer.render_template('chats.html', dest_file,
                                            context)
        self.engine.dispose()


def chat_worker(data):
    worker = ChatWorker(report_bundle=data['report_bundle'])
    worker.run(data['chat_id'])
