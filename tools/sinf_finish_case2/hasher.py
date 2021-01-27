import hashlib
import hashlib
from helpers import *
import logging
from portable import PortableHandler
from tqdm import tqdm


class Hasher:
    def __init__(self):
        self.total = 0
        self.count = 0
        self.put_portable = True
        self.images_partial = True
        self.iped_partial = True
        self.hash_file = None
        self._root = None
        self.log_file_path = None
        self.logger = None
        self.only_count = False
        self.root = "."
        self.portable_handler = PortableHandler()
        self.pbar = None
        self.verbose = False

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = Path(value)
        self.hash_file_path = self._root / "hash.txt"
        self.log_file_path = self.root / "hashlog.log"
        # self.logger = get_logger(self.log_file_path)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def sha512(self, path: Path, extra=False):
        if not extra and path == self.hash_file_path:
            return
        if self.only_count:
            self.total += 1
            return
        hash_sha512 = hashlib.sha512()
        if self.verbose:
            print(f"Calculando: \"{path}\"")
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        res = hash_sha512.hexdigest()
        if not extra:
            self.pbar.update(1)
        return res

    def hash_folder(self, folder: Path):
        res = is_iped_ignore(folder)
        if res:
            if self.put_portable:
                self.logger.info(f"Colocando {folder.parent} portável.")
                self.portable_handler.put_portable(folder.parent)
            if self.iped_partial:
                if not self.only_count:
                    self.logger.info(f"DESCONSIDERANDO: {folder}")
                return
        
        # Testar permissão de acesso a pasta
        try:
            for entry in folder.iterdir():
                break
        except PermissionError:
            self.logger.info(f"Erro de permissão ao tentar acessar a pasta \"{folder}\"")
            return


        for entry in folder.iterdir():
            if entry.is_dir():
                self.hash_folder(entry)
            else:
                if self.images_partial and is_e01_partial(entry):
                    if not self.only_count:
                        self.logger.info(f"DESCONSIDERANDO: {entry}")
                    return
                try:
                    res = self.sha512(entry)
                    if res:
                        self.hash_file.write(
                            f"{res}     {entry.relative_to(self._root)}\n")
                except (FileNotFoundError, OSError) as e:
                    self.logger.error(str(e))

    def run(self):
        self.only_count = False
        self.pbar = tqdm(total=self.total)
        with self.hash_file_path.open("w", encoding="utf-8") as f:
            self.hash_file = f
            self.logger.info("Iniciando...")
            self.hash_folder(self.root)
        self.pbar.close()
        res = self.sha512(self.hash_file_path, extra=True)
        print("\nHash do hash:")
        print(res)

    def count_files(self):
        self.only_count = True
        print("Contanto arquivos, pode demorar, aguarde...")
        self.hash_folder(self.root)
        self.only_count = False
