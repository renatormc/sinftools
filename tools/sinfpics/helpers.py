from sinf_requests import Requester
import config
import zipfile
import tempfile
from pathlib import Path
import os
from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2
import re


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


def upload_fotos(folder, alias):
    tempzip = Path(tempfile.gettempdir()) / "sinfpics.zip"
    zip_folder(str(folder), str(tempzip))
    files = {'file': (tempzip.name, tempzip.open("rb"), 'application/zip')}
    req = Requester()
    url = f"{config.url_sinfweb}/organizador/upload-fotos/{alias}"
    res = req.post(url, files=files)
    return res.status_code
   

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

class NameAnalyzer:
    def __init__(self):
        self.reg = re.compile(r'((^[A-Za-z]+)([\d\.]+))(?:_(\d*))?')

    def analise_name(self, name):
        res = self.reg.search(name)
        if not res:
            return
        ret = {
            'alias': res.group(2),
            'obj_number': res.group(3),
            'pic_seq': res.group(4)
        }
        if ret['obj_number'] is not None:
            return ret

def check_pics(folder: Path):
    analyzer = NameAnalyzer()
    exts = ['.jpg', '.png']
    alias = []
    errors = []
    for entry in folder.iterdir():
        if entry.is_dir():
            errors.append(f"{entry.name} é um diretório. Somente arquivos são aceitos dentro da pasta de fotos.")
            continue
        if entry.name.startswith("_"):
            continue
        if entry.suffix.lower() not in exts:
            errors.append(f"Arquivo {entry.name} é de um tipo não aceito. Somente jpg e png são aceitos.")
            continue
        res = analyzer.analise_name(entry.name)
        if not res:
            errors.append(f"O arquivos {entry.name} não está nomeado no padrão de nomes exigido.")
            continue
        if res['alias'] not in alias:
            alias.append(res['alias'])
    if len(alias) > 1:
        aux = ",".join(alias)
        errors.append(f"Foram encontradas fotos de mais de uma perícia ({aux}). Somente é aceito uma perícia por pasta")
    alias = alias[0] if alias else None
    return alias, errors


if __name__ == "__main__":
    print(zip_folder("C:"))
