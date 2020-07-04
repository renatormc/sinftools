import requests
from sinf.servers import config
from sinf.servers.com import get_user_chat_id

base_url = "https://api.telegram.org/bot1265537046:AAHBVh5zx7VUld7e0y9Vf8VjOVgo8_dSMHc"

def url(url):
    return f"{base_url}{url}"

class UserNotRegistered(Exception):
    pass

def get_updates():
    resp = requests.get(url("/getUpdates"))
    return resp.json()

def get_users_updates():
    resp = requests.get(url("/getUpdates"))
    users = {}
    for item in resp.json()['result']:
        chat = item['message']['chat']
        user = {
            "username": chat['username'],
            "chat_id": chat['id']
        }
        if not user['chat_id'] in users.keys():
            users[user['chat_id']] = user
    return list(users.values())

def send_message(username, text):
    try:
        chat_id = get_user_chat_id(username)
        resp = requests.get(url("/sendMEssage"), params={'chat_id' : chat_id, 'text': text})
        return resp.json()
    except KeyError:
        raise UserNotRegistered(f"Usuário \"{username}\" não cadastrado.")

if __name__ == "__main__":
    res = send_message('renao', "E ai")
    print(res)