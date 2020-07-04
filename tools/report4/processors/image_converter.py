from models import *
from database import db_session
from PIL import Image
from pathlib import Path
from config_manager import config_manager


class ImageConverter:
    def __init__(self, read_source):
        self.read_source = read_source

    def run(self):
        extensions = config_manager.file_types['browser_supported']['image']
        files = db_session.query(File).filter(File.type_ == 'image', ~File.extension.in_(extensions)).all()
        for file in files:
            try:
                path = Path(file.path)
                new_path = path.with_suffix('.jpg')
                im = Image.open(path).convert("RGB")
                im.save(new_path, "jpeg")
                file.converted_path = new_path
                db_session.add(file)
            except Exception as e:
                print(e)
                print(f"Erro ao converter arquivo de imagem {path}")
        db_session.commit()