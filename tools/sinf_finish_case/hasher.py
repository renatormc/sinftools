from pathlib import Path
import config
import markers
import hashlib
from portable import put_portable
import logging


class Hasher:

    def __init__(self):
        self.f = None
        self.n_files = 0

    def hash_folder(self, folder: Path):
        pass

    @staticmethod
    def sha512(fname):
        if fname.endswith(".sinf_mark.json"):
            return
        print(f"Calculando hash de \"{fname}\"")
        hash_sha512 = hashlib.sha512()
        try:
            with open(fname, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha512.update(chunk)
        except (FileNotFoundError, OSError) as e:
            logger.error(str(e))

        return hash_sha512.hexdigest()
