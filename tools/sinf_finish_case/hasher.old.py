from pathlib import Path
import config
import markers
import hashlib
from portable import put_portable
from logger import get_logger
from tqdm import tqdm


def sha512(path):
    path = Path(path)
    hash_sha512 = hashlib.sha512()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)
    return hash_sha512.hexdigest()


class Hasher:

    def __init__(self, folder):
        self.f = None
        self.only_count = False
        self.n_files = 0
        self.root = Path(folder)
        self.hash_file = self.root / "hash.txt"
        self.pbar = None
        self.logger = get_logger(self.root / "hash.log")


    def calc_hash_file(self, path: Path):
        if path.name == ".sinf_mark.json":
            return
        if self.only_count:
            self.n_files += 1
            print(f"{self.n_files}\r", end='')
            return
        try:
            text = sha512(path)
            self.f.write(f"{text}     {path.relative_to(self.root)}\n")
        except (FileNotFoundError, OSError) as e:
            self.logger.error(str(e))
        
        self.pbar.update(1)

    @staticmethod
    def __is_hash_partial(path: Path):
        markers_ = markers.get_markers_folder(path)
        for marker in markers_:
            if marker and marker['type'] == "hash_partial":
                return marker['subtype']

    def hash_normal_folder(self, folder: Path):
        try:
            for entry in folder.iterdir():
                if entry.is_dir():
                    self.hash_folder(entry)
                else:
                    self.calc_hash_file(entry)
        except (FileNotFoundError, OSError) as e:
            self.logger.error(str(e))

    def hash_folder_iped_images(self, folder: Path):
        try:
            for item in folder.iterdir():
                if item.is_file() and item.suffix in [".log", ".txt"]:
                    self.calc_hash_file(item)
                elif item.is_dir():
                    self.hash_folder(item)
        except (FileNotFoundError, OSError) as e:
            self.logger.error(str(e))

    def hash_folder_iped_results(self, folder: Path):
        item = folder / "FileList.csv"
        if not item.exists():
            item = item / "Lista de Arquivos.csv"
        if item.exists():
            self.calc_hash_file(item)
        put_portable(folder)

    def hash_folder(self, folder: Path):
        type_ = self.__is_hash_partial(folder)
        if type_ == "iped_results":
            self.hash_folder_iped_results(folder)
        elif type_ == "iped_images":
            self.hash_folder_iped_images(folder)
        else:
            self.hash_normal_folder(folder)

    def count_files(self):
        print("Contando arquivos")
        self.only_count = True
        self.hash_folder(self.root)
        self.only_count = False
        print(f"{self.n_files} arquivos encontrados")

    def run(self):
        self.count_files()
        self.logger.info("Inciando")
        try:
            self.f = self.hash_file.open("w", encoding="utf-8")
            self.pbar = tqdm(total=self.n_files)
            self.hash_folder(self.root)
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

