import hashlib




def sha512(fname, only_count=False):
    if only_count or fname == "log.log" or fname == "hash.txt":
        return
    hash_sha512 = hashlib.sha512()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)
    return  hash_sha512.hexdigest()
