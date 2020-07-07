import requests
import os
from pathlib import Path
from datetime import datetime
import jwt

sinftools_dir = Path(os.getenv("SINFTOOLS"))


class TokenExpiredException(Exception):
    pass


class TokenNoFoundException(Exception):
    pass


class Requester:

    def __init__(self, token):
        self.token = token
        if isinstance(token, Path):
            self.__load_token_from_file(token)

    def __load_token_from_file(self, path):
        if not path.exists():
            raise TokenNoFoundException("Token file not found")
        now = datetime.now()
        token = path.read_text(encoding="utf-8")
        headers = jwt.get_unverified_header(token)
        try:
            if headers['exp'] < datetime.timestamp(now):
                raise TokenExpiredException("Exxpired token")
        except KeyError:
            pass
        self.token = token

    def get(self, url, headers={}, *args, **kargs):
        headers['Authorization'] = f"Bearer {self.token}"
        return requests.get(url, headers=headers, *args, **kargs)

    def post(self, url, headers={}, *args, **kargs):
        headers['Authorization'] = f"Bearer {self.token}"
        return requests.post(url, headers=headers, *args, **kargs)

    def delete(self, url, headers={}, *args, **kargs):
        headers['Authorization'] = f"Bearer {self.token}"
        return requests.delete(url, headers=headers, *args, **kargs)

    def patch(self, url, headers={}, *args, **kargs):
        headers['Authorization'] = f"Bearer {self.token}"
        return requests.patch(url, headers=headers, *args, **kargs)
