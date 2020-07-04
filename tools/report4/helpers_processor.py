import re
import os
import pathlib
from config_manager import config_manager


def get_file_type(file_):
    ext = pathlib.Path(file_.extracted_path).suffix
    extensions = config_manager.file_types
    if ext.lower() in extensions['image']:
        type_ = 'image'
    elif ext.lower() in extensions['video']:
        type_ = 'video'
    elif ext.lower() in extensions['audio']:
        type_ = 'audio'
    elif file_.content_type and 'image' in file_.content_type:
        type_ = 'image'
    elif file_.content_type and 'video' in file_.content_type:
        type_ = 'video'
    elif file_.content_type and 'audio' in file_.content_type:
        type_ = 'audio'
    else:
        type_ = 'file'
    return type_

def get_avatar(identifier, device_folder):
    if not identifier:
        return
    identifier = get_short_identifier(identifier)
    folders = [os.path.join(device_folder, 'Avatars'), os.path.join(device_folder, 'Profile')]
    for folder in folders:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                if identifier in f:
                    return os.path.join(folder, f)


def get_short_identifier(identifier):
    if "@s.whatsapp.net" in identifier or "@g.us" in identifier:
        return identifier.split("@")[0]
    elif "@" in identifier and "whatsapp" in identifier:
        parts = identifier.split("@")
        return parts[0]
    return identifier


def get_avatar_android(identifier):
    res = re.search(r'((.*)@s.whatsapp.net)(.*)', identifier)
    if res:
        if res.groups()[0].strip() != '':
            return res.groups()[0].strip() + ".jpg"
        else:
            return ''
    else:
        res = re.search(r'((.*)@g.us)(.*)', str(identifier))
        if res:
            if res.groups()[0].strip() != '':
                return res.groups()[0].strip() + ".jpg"
            else:
                return ''
        else:
            return ''


def get_avatar_iphone(identifier):
    if "@" in identifier and "whatsapp" in identifier:
        parts = identifier.split("@")
        return f"{parts[0]}.jpg"
    return f"desconhecido.jpg"


def get_friendly_identifier(identifier, name):
    identifier = identifier.strip() if identifier else ""
    name = name.strip() if name else ""
    if name == identifier:
        name = ""
    number = ""
    if "@s.whatsapp" in identifier:
        number = identifier.split("@")[0] or ""
    elif "ONE_TO_ONE" in identifier:
        number = identifier.split(":")[1] or ""
    elif identifier:
        return identifier
    return f"{number} {name}" if name or number else "Desconhecido"


def find_out_avatars_folder():
    if os.path.exists('Avatars'):
        files = os.listdir('Avatars')
        n = len(files)
        n2 = 0
        for file_ in os.listdir('Avatars'):
            if file_.endswith('.j') and 'whatsapp' in file_:
                n2 += 1
        if n2 / n > 0.7:
            return 'Avatars', 'Android'
    elif os.path.exists('Profile'):
        files = os.listdir('Profile')
        n = len(files)
        n2 = 0
        for file_ in os.listdir('Avatars'):
            # verifica se a quantidade de digitos numericos no nome do arquivo é grande
            n3 = sum(c.isdigit() for c in file_)
            if n3 / len(file_) > 0.7 and "jpg" in file_.lower():
                n2 += 1
        if n2 / n > 0.7:
            return 'Profile', 'Iphone'


def rename_avatars():
    folders = ['Avatars', 'Profile']
    for folder in folders:
        if os.path.exists(folder):
            for f in os.listdir(folder):
                p = pathlib.Path(folder, f)
                if len(p.suffix) < 3:
                    p.rename(p.with_suffix('.jpg'))


def get_last_avatar_names(dir_):
    files = os.listdir(dir_)
    contacts = []
    for filename in files:
        parts = filename.split("-")
        if len(parts) == 2:
            contact = parts[0]
        elif len(parts) == 3:
            contact = f"{parts[0]}-{parts[1]}"
        if contact not in contacts:
            contacts.append(contact)

    avatars = []
    for contact in contacts:
        avatar = None
        for item in filter(lambda x: x.startswith(contact), files):
            timestamp = item.replace(
                f"{contact}-", "").replace(".jpg", "").replace(".thumb", "")
            try:
                timestamp = int(timestamp)
            except:
                continue
            if avatar is None:
                avatar = (item, timestamp, contact)
                continue
            if avatar[1] < timestamp:
                avatar = (item, timestamp, contact)
        avatars.append(avatar)
    return avatars


if __name__ == "__main__":
    os.chdir(
        r'C:\Users\renato\laudos\trabalhando\46.6303.2019\midia\C2\2019-02-11.12-56-11\Samsung GSM_SM-G532M Galaxy J2 Prime')
    print(find_out_avatars_folder())
