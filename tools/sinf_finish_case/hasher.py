from pathlib import Path
import config
import markers
import hashlib
from portable import put_portable
from logger import get_logger
from tqdm import tqdm
import multiprocessing


def sha512(path):
    path = Path(path)
    hash_sha512 = hashlib.sha512()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)
    return hash_sha512.hexdigest()


def calc_hash(path):
    path = Path(path)
    try:
        text = sha512(path)
        return path, text, None
    except (FileNotFoundError, OSError) as e:
        return path, "", e


class Hasher:

    def __init__(self, folder):
        self.f = None
        self.n_files = 0
        self.root = Path(folder)
        self.hash_file = self.root / "hash.txt"
        self.pbar = None
        self.logger = get_logger(self.root / "hash.log")
        self.n_workers = 4


    def check_file(self, path: Path):
        if path.name == ".sinf_mark.json":
            return False
        return True
       

    @staticmethod
    def __is_hash_partial(path: Path):
        markers_ = markers.get_markers_folder(path)
        for marker in markers_:
            if marker and marker['type'] == "hash_partial":
                return marker['subtype']

    def hash_normal_folder(self, folder: Path):
        for entry in folder.iterdir():
            if entry.is_dir():
                for item in self.hash_folder(entry):
                    yield item
            else:
                if self.check_file(entry):
                    yield entry
      

    def hash_folder_iped_images(self, folder: Path):
        for item in folder.iterdir():
            if item.is_file() and item.suffix in [".log", ".txt"]:
                if self.check_file(item):
                    yield item
            elif item.is_dir():
                for item in self.hash_folder(item):
                    yield item
    
      
    def hash_folder_iped_results(self, folder: Path):
        put_portable(folder)
        item = folder / "FileList.csv"
        if not item.exists():
            item = item / "Lista de Arquivos.csv"
        if item.exists():
            if self.check_file(item):
                yield item
           
        

    def hash_folder(self, folder: Path):
        type_ = self.__is_hash_partial(folder)
        if type_ == "iped_results":
            for item in self.hash_folder_iped_results(folder):
                yield item
        elif type_ == "iped_images":
            for item in self.hash_folder_iped_images(folder):
                yield item
        else:
            for item in self.hash_normal_folder(folder):
                yield item


    def count_files(self):
        print("Contando arquivos")
        self.n_files = 0
        for item in self.hash_folder(self.root):
            self.n_files += 1
        print(f"{self.n_files} arquivos encontrados")



    def run(self):
        self.count_files()
        self.logger.info("Inciando")
        try:
            self.f = self.hash_file.open("w", encoding="utf-8")
            self.pbar = tqdm(total=self.n_files)
            pool = multiprocessing.Pool(processes=self.n_workers)
            for path, hash_, err in pool.imap(calc_hash, self.hash_folder(self.root)):
                if err:
                    self.logger.error(str(err))
                else:
                    self.f.write(f"{hash}     {path.relative_to(self.root)}\n")
                self.pbar.update(1)
            self.pbar.close()
        finally:
            self.f.close()
        res = sha512(self.hash_file)
        print("Hash do hash")
        print(res)
        self.logger.info("Finalizado")
        self.logger.info(f"Hash do hash: {res}")
        


if __name__ == "__main__":
    hasher = Hasher('.')
    hasher.run()

