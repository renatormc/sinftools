import hashlib
from pathlib import Path

class HashCalc:
    def __init__(self):
        self.hashes = []
        self.files= None
        self.hash_file = None

    def set_files(self, files):
        self.files = files

    def set_hash_file(self, file):
        self.hash_file = file


    def sha512(self, fname):
        hash_sha512 = hashlib.sha512()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()

