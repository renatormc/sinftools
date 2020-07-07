import requests
import os

class Requester:

    def __init__(self, token):
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
