from models import *
from database import db_session
from database import db_connect
from config_manager import config_manager
from helpers_cmd import progress
from thumbs_generator import ThumbsGenerator
from pathlib import Path
from multiprocessing import Pool

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def worker(data):
    engine, dbsession = db_connect()
    thumbs_generator = data[0]
    chunk = data[1]
    for file_ in chunk:
        file = dbsession.query(File).get(file_[0])
        filename = thumbs_generator.generate_image_thumb(file.path)
        if filename:
            file.analise_thumb = Path(filename).name
            file.corrupted = False
        else:
            file.analise_thumb = None
            file.corrupted = True
        dbsession.add(file)
    dbsession.commit()
    engine.dispose()

    

class ThumbImage:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        if not config_manager.data['thumbnails']['image']:
            return
        folder = Path(self.read_source.folder) / "sinf_thumbs"
        thumbs_generator = ThumbsGenerator(folder)
        thumbs_generator.set_config(
            n_rows=config_manager.data['thumbnails']['n_rows'], n_cols=config_manager.data['thumbnails']['n_cols'],
            thumb_size=config_manager.data['thumbnails']['image_thumb_size'],
            extension=config_manager.data['thumbnails']['extension'])

        files = db_session.query(File.id).filter_by(type_='image').filter(
            File.extracted_path != None, File.read_source == self.read_source).all()
       
        print("\nGerando thumbs das imagens")
        chunks_ = list(chunks(files, 100))
        n = len(chunks_)
        n_workers = config_manager.n_workers
        procs = ((thumbs_generator, chunk) for chunk in chunks_)
        if n_workers > 1:
            pool = Pool(processes=n_workers)
            for i, _ in enumerate(pool.imap_unordered(worker, procs)):
                progress(i, n)
            pool.close()
            pool.join()
        else:
            for i, proc in enumerate(procs):
                worker(proc)
                progress(i, n)
