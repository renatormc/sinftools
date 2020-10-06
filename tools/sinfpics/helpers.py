from sinf_requests import Requester
import config
import zipfile
import tempfile
from pathlib import Path
import os
from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2


def get_pericias():
    req = Requester()
    url = f"{config.url_sinfweb}/organizador/pericias-andamento-perito"
    res = req.get(url)
    if res.status_code == 200:
        items = res.json()
        return [f"{item['id_texto']} - {item['alias']}" for item in items]
    else:
        return []


def to_text_id(value):
    return value.split("-")[0].strip()


def zip_folder(folder_path, output_path):
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(folder_path + '\\','')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(folder_path + '\\','')

                zip_file.write(absolute_path, relative_path)
    finally:
        zip_file.close()


def upload_fotos(folder, pericia):
    tempzip = Path(tempfile.gettempdir()) / "sinfpics.zip"

    zip_folder(str(folder), str(tempzip))

    # zipf = zipfile.ZipFile(tempzip, 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in os.walk(folder):
    #     for file in files:
    #         zipf.write(os.path.join(root, file), file)

    files = {'file': (tempzip.name, tempzip.open("rb"), 'application/zip')}
    req = Requester()
    url = f"{config.url_sinfweb}/organizador/upload-fotos"
    res = req.post(url, files=files, data={'pericia': pericia})
    if res.status_code == 200:
        return True
    else:
        return False

def escolher_pericia():
    pericias = get_pericias()
    questions = [
        {
            'type': 'list',
            'name': 'pericia',
            'message': 'Selecione a perícia: ',
            'choices': pericias
        },
    ]

    answers = prompt(questions, style=custom_style_2)
    return answers['pericia']


if __name__ == "__main__":
    print(zip_folder("C:"))
