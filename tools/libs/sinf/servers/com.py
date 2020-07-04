import requests
from requests.exceptions import ConnectionError, ReadTimeout
from sinf.servers import config
from pathlib import Path
import json
import urllib.request
from sinf.servers.repo import get_telegram_broken_url
from sinf.servers.auth import get_acess_token

path_telegram_users = config.app_dir / "telegram_users.json"



def get_user_chat_id(username):
    username = username.lower().strip()
    with path_telegram_users.open("r", encoding="utf-8") as f:
        data = json.load(f)
    try:
        return data[username]
    except KeyError:
        return None

def register_user(username, chat_id):
    username = username.lower().strip()
    with path_telegram_users.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data[username] = chat_id
    with path_telegram_users.open("w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=4))
   

def send_message(username, text):
    try:
        username = username.lower().strip()
        telegram_broken_url = get_telegram_broken_url()
        if not telegram_broken_url:
            return False
        url = f"{telegram_broken_url}/send-telegram"
        response = requests.post(url, json={'username': username, 'text': text}, timeout=5)
        print(response.status_code)
        if response.status_code == 200:
            return True
        return False
    except (ConnectionError, ReadTimeout) as e:
        print(e)
        return False


def request_check_process():
    url = f"http://localhost:8002/check-process"
    response = requests.get(url, timeout=5)
   
   
def has_internet(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def check_telegram_broken():
    if not config.this_server_config:
        return
    if has_internet():
        for server, data in config.servers.items():
            try:
                
                payload = {"value": config.this_server_config['url']}
                url = f"{data['url']}/set-telegram-broken-url"
                response = requests.post(url, json=payload, timeout=5)
            except (ConnectionError, ReadTimeout) as e:
                print(e)
            

def request_get(url, *args, timeout=config.timeout, **kargs):
    headers = {
        'Authorization': f"Bearer {get_acess_token()}"}
    return requests.get(url, *args, timeout=timeout, headers=headers, **kargs)


def request_post(url, *args, timeout=config.timeout, **kargs):
    headers = {
        'Authorization': f"Bearer {get_acess_token()}"}
    return requests.post(url, *args, timeout=timeout, headers=headers, **kargs)