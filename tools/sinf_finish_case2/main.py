from helpers import *
from logger import logger
import hashlib
from portable import *


class Processor:
    def __init__(self):
        self.total = 0
        self.count = 0
        self.put_portable = True
        self.images_partial = True
        self.iped_partial = True
        self.hash_file = None
        self._root = None
        self.only_count = False
        self.root = "."
        self.log_file_path = self.root / "hashlog.log"

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = Path(value)
        self.hash_file_path = self._root / "hash.txt"
        self.hash_hash_file_path = self._root / "../hash_do_hash.txt"

    def sha512(self, path: Path):
        if self.only_count:
            self.total += 1
            return
        if path == self.hash_file_path or path == self.log_file_path:
            return
        hash_sha512 = hashlib.sha512()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()

    def hash_folder(self, folder: Path):
        if self.iped_partial and is_iped_results_folder(folder):
            if self.put_portable:
                put_portable(folder.parent)
        for entry in folder.iterdir():
            if entry.is_dir():
                self.hash_folder(entry)
            else:
                try:
                    res = self.sha512(entry)
                    self.hash_file.write(
                        f"{res}     {entry.relative_to(self._root)}\n")
                except (FileNotFoundError, OSError) as e:
                    logger.error(str(e))

    def run(self):
        self.only_count = False
        with self.hash_file_path.open("w", encoding="utf-8") as f:
            self.hash_file = f
            logger.info("Iniciando...")
            self.hash_folder(self.root)

    def count_files(self):
        self.only_count = True
        print("Contanto arquivos, pode demorar, aguarde...")
        self.hash_folder(self.root)
        self.only_count = False
