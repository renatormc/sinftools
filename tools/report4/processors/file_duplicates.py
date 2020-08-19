from models import *
from database import db_session, db_connect
from helpers_cmd import progress
from multiprocessing import Pool
from config_manager import config_manager


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def worker(chunk):
    engine, dbsession = db_connect()
    for item in chunk:
        attachment = dbsession.query(File).get(item[0])
        file_ = dbsession.query(File).filter(
            File.message_id == None, File.extracted_path == attachment.extracted_path, File.read_source_id == attachment.read_source_id).first()
        if file_:
            attachment.size = attachment.size or file_.size
            attachment.filename = attachment.filename or file_.filename
            attachment.original_path = attachment.original_path or file_.original_path
            attachment.extracted_path = attachment.extracted_path or file_.extracted_path
            attachment.content_type = attachment.content_type or file_.content_type
            attachment.creation_time = attachment.creation_time or file_.creation_time
            attachment.access_time = attachment.access_time or file_.access_time
            attachment.sha256 = attachment.sha256 or file_.sha256
            attachment.md5 = attachment.md5 or file_.md5
            attachment.deleted_state = attachment.deleted_state or file_.deleted_state
            attachment.type_ = attachment.type_ or file_.type_
            attachment.page_renderized = attachment.page_renderized or file_.page_renderized
            attachment.analise_thumb = attachment.analise_thumb or file_.analise_thumb
            attachment.corrupted = attachment.corrupted or file_.corrupted
            dbsession.add(attachment)
            dbsession.delete(file_)
    dbsession.commit()
    engine.dispose()

class FileDuplicates:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        print("Excluindo entradas de arquivos duplicadas no DB")
        attachments = db_session.query(File.id).filter(
            File.message_id != None, File.read_source_id == self.read_source.id).all()
        chunks_ = list(chunks(attachments, 100))
        n = len(chunks_)
        n_workers = config_manager.n_workers
        if n_workers > 1:
            pool = Pool(processes=n_workers)
            for i, _ in enumerate(pool.imap_unordered(worker,chunks_)):
                progress(i, n)
            pool.close()
            pool.join()
        else:
            for i, chunk in enumerate(chunks_):
                worker(chunk)
                progress(i, n)
        # n = len(attachments)
        # for i, attachment in enumerate(attachments):
        #     progress(i, n)
        #     file_ = db_session.query(File).filter(
        #         File.message_id == None, File.extracted_path == attachment.extracted_path, File.read_source_id == attachment.read_source_id).first()
        #     if file_:
        #         attachment.size = attachment.size or file_.size
        #         attachment.filename = attachment.filename or file_.filename
        #         attachment.original_path = attachment.original_path or file_.original_path
        #         attachment.extracted_path = attachment.extracted_path or file_.extracted_path
        #         attachment.content_type = attachment.content_type or file_.content_type
        #         attachment.creation_time = attachment.creation_time or file_.creation_time
        #         attachment.access_time = attachment.access_time or file_.access_time
        #         attachment.sha256 = attachment.sha256 or file_.sha256
        #         attachment.md5 = attachment.md5 or file_.md5
        #         attachment.deleted_state = attachment.deleted_state or file_.deleted_state
        #         attachment.type_ = attachment.type_ or file_.type_
        #         attachment.page_renderized = attachment.page_renderized or file_.page_renderized
        #         attachment.analise_thumb = attachment.analise_thumb or file_.analise_thumb
        #         attachment.corrupted = attachment.corrupted or file_.corrupted
        #         db_session.add(attachment)
        #         db_session.delete(file_)
        # db_session.commit()