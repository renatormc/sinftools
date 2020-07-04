import hashlib
import base64
import os

def hash_worker(path):
    m = hashlib.sha256()
    m.update(path.open('rb').read())
    return (str(base64.b64encode(m.digest()))[2:-1], path)

    