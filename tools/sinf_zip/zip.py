import zipfile
import os
import sys
import json
import codecs
import shutil
from datetime import datetime
from renderizer import Renderizer
script_dir = os.path.dirname(os.path.realpath(__file__))
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_1
from sinf.hash import Hasher
import configparser
from sinf.inquirer.inquirer import get_answaers
from pathlib import Path
from pyfiglet import Figlet


# import argparse

dir_sinftools = os.getenv("SINFTOOLS")
# parser = argparse.ArgumentParser()
# parser.add_argument("dir", help="Dir to be zipped")
# parser.add_argument("-t", "--type", action="store", default="7zip", choices=['7zip', 'rar', 'sinf'], help="Compress type")
# parser.add_argument("--midia", action="store", default="DVD", choices=['DVD', 'CD'], help="Midia type")
# parser.add_argument("--level", action="store", default="3", type=int, choices=[0,1,2,3,4,5], help="Level of compression")
# parser.add_argument("--hash", action="store_true", help="Calculate hash before compress.")
# args = parser.parse_args()

dirs = ["."]
for entry in os.listdir():
    if os.path.isdir(entry):
        dirs.append(entry)

# options = {
#     "7zip com tutorial na mídia": '7zip',
#     "rar com tutorial na mídia": 'rar',
#     "7zip com copiador da sinf (não precisa de tutorial)": 'sinf'
# }
options = {
     "7zip": 'sinf',   
}
reverse_options = {v:k for k, v in options.items()}

config_form = {
    "label": "Preencha os dados",
    "items": [
        {
            "type": "combo",
            "name": "dir",
            "label": "Diretório que contém os arquivos a serem comprimidos",
            "list": dirs,
            "default": '.',
            "row": 1,
            "stretch": 1
        },
        {
            "type": "combo",
            "name": "type",
            "label": "Tipo de compressão",
            "list": list(options.keys()),
            "default": reverse_options["sinf"],
            "editable": False,
            "row": 1,
            "stretch": 1
        },
        {
            "type": "combo",
            "name": "midia",
            "label": "Tipo de mídia",
            "list": ["DVD", "CD"],
            "default": "DVD",
            "row": 2,
            "stretch": 1
        },
        {
            "type": "combo",
            "name": "level",
            "label": "Nível de compressão",
            "list": ["0", "1", "2", "3", "4", "5"],
            "default": "3",
            "converter": "integer",
            "row": 2,
            "stretch": 1
        },
        {
            "type": "checkbox",
            "name": "hash",
            "label": "Calcular hash antes de compactar",
            "default": False,
            "row": 3,
            "stretch": 1
        }
    ]
}

answers = get_answaers(config_form)
if answers:
    answers['type'] = options[answers['type']]


def get_number(filename):
    val = filename.replace("dados.part", "").split(".")[0]
    return int(val)


if answers:
    dvd_size = 4300*1024*1024
    cd_size = 670*1024*1024

    midia_sizes = {
        'DVD': dvd_size,
        'CD': cd_size
    }

    folder = answers['dir']
    output_folder = "..\\midias_para_gravar" if answers['dir'] == '.' else ".\\midias_para_gravar"
    max_size = midia_sizes[answers['midia']]
    begin_time = datetime.now()


    if answers['hash']:
        print("Calculando hash")
        hasher = Hasher()
        hasher.directory = answers['dir']
        hasher.directory_hash_hash = os.path.join(answers['dir'], '..')
        hasher.calculaHashes()
        hasher.calculaHashDoHash()

    print("Iniciando compressão")
    if answers['type'] == '7zip':
        print("Comprimindo 7zip")
        level_dict = {
            0: 0,
            1: 1,
            2: 3,
            3: 5,
            4: 7,
            5: 9
        }
        level_compression = level_dict[answers['level']]
        sevenzipexe = f'{dir_sinftools}\\extras\\7-ZipPortable\\App\\7-Zip64\\7z.exe'
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.mkdir(output_folder)
        cmd = f"{sevenzipexe} a -v{max_size}b -mx{level_compression} -sfx7z.sfx {output_folder}\\dados.exe \"{os.path.abspath(folder)}\""
        os.system(cmd)
        files = os.listdir(output_folder)
        n = len(files)
        if n > 2:

            # renderizar tutorial
            midias = []
            for file in files:
                if not file.endswith("exe"):
                    end_ = file[-3:]
                    if end_ == "001":
                        midias.append({'name': f"MIDIA {end_}", 'files': [
                                    'dados.exe', f'dados.7z.{end_}']})
                    else:
                        midias.append({'name': f"MIDIA {end_}",
                                    'files': [f'dados.7z.{end_}']})
            renderizer = Renderizer()
            renderizer.render_template('tutorial_template_7zip.html', f'{script_dir}\\tutorial_renderizado.html', {
                                    'midias': midias, 'n_midias': len(midias)})

            dir_ = f"{output_folder}\\001"
            if not os.path.exists(dir_):
                os.mkdir(dir_)
            shutil.move(f"{output_folder}\\dados.exe", f"{dir_}\\dados.exe")
            for file in files:
                if not file.endswith("exe"):
                    dir_ = f"{output_folder}\\{file[-3:]}"
                    if not os.path.exists(dir_):
                        os.mkdir(dir_)
                    shutil.move(f"{output_folder}\\{file}", f"{dir_}\\{file}")
                shutil.copy(f"{script_dir}\\tutorial_renderizado.html",
                            f"{dir_}\\Como vizualizar os dados.html")
    elif answers['type'] == 'rar':
        print("Comprimindo rar")
        winrarexe = f'{dir_sinftools}\\tools\\winrar\\Rar.exe'
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.mkdir(output_folder)
        cmd = f"{winrarexe} a -m{answers['level']} -v{max_size}b -o+ -ep1 -r -t -sfx {output_folder}\\dados.exe \"{folder}\""
        print(cmd)
        os.system(cmd)
        files = [f for f in os.listdir(output_folder) if "dados.part" in f]
        n = len(files)
        if n > 1:
            # renderizar tutorial
            files_on_midia = []
            for file in files:
                files_on_midia.append(
                    {'midia': f"MIDIA {get_number(file)}", 'name': file})
            renderizer = Renderizer()
            renderizer.render_template('tutorial_template.html', f'{script_dir}\\tutorial_renderizado.html', {
                                    'files': files_on_midia, 'n_midias': len(files)})

            files = {get_number(file): file for file in files}
            for key, value in files.items():
                dir_ = f"{output_folder}\\{key}"
                os.mkdir(dir_)
                shutil.move(f"{output_folder}\\{value}", f"{dir_}\\{value}")
                shutil.copy(f"{script_dir}\\tutorial_renderizado.html",
                            f"{dir_}\\Instruções.html")
    elif answers['type'] == 'sinf':
        print("Comprimindo custom sinf")
        level_dict = {
            0: 0,
            1: 1,
            2: 3,
            3: 5,
            4: 7,
            5: 9
        }
        level_compression = level_dict[answers['level']]
        sevenzipexe = f'{dir_sinftools}\\extras\\7-ZipPortable\\App\\7-Zip64\\7z.exe'
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.mkdir(output_folder)
        cmd = f"{sevenzipexe} a -v{max_size}b -mx{level_compression} -sfx7z.sfx {output_folder}\\dados.exe \"{os.path.abspath(folder)}\""
        os.system(cmd)

        files = os.listdir(output_folder)
        n = len(files)
        if n > 2:

            # renderizar tutorial
            midias = []
            for file in files:
                if not file.endswith("exe"):
                    end_ = file[-3:]
                    if end_ == "001":
                        midias.append({'name': f"MIDIA {end_}", 'files': [
                                    'dados.exe', f'dados.7z.{end_}']})
                    else:
                        midias.append({'name': f"MIDIA {end_}",
                                    'files': [f'dados.7z.{end_}']})
            renderizer = Renderizer()
            renderizer.render_template('tutorial_template_sinf.html', f'{script_dir}\\tutorial_renderizado.html', {
                                    'midias': midias, 'n_midias': len(midias)})

           
            midias = {1: []}
            dir_ = f"{output_folder}\\1\\.sinf"
            if not os.path.exists(dir_):
                os.makedirs(dir_)
            files = [file for file in os.listdir(output_folder) if "dados." in file]
            for file in files:
                if os.path.isdir(f"{output_folder}\\{file}"):
                    continue
                if file.endswith("exe"):
                    midias[1].append(file)
                    dir_ = f"{output_folder}\\1"
                    shutil.move(f"{output_folder}\\{file}", f"{dir_}\\{file}")
                else:
                    number = int(file.split(".")[-1])
                    if number in midias.keys():
                        midias[number].append(file)
                    else:
                        midias[number] = [file]
                    dir_ = f"{output_folder}\\{number}"
                    if not os.path.exists(dir_):
                        os.makedirs(dir_)
                    shutil.move(f"{output_folder}\\{file}", f"{dir_}\\{file}")


            for key, value in midias.items():
                lines = [",".join(value) for value in midias.values()]
                text = "\n".join(lines)
                hidden_folder = Path(output_folder, str(key), ".sinf")
                if not hidden_folder.exists():
                    os.makedirs(hidden_folder)
                with (hidden_folder / "midias.txt").open("w") as f:
                    f.write(text)
                # with codecs.open(os.path.join(output_folder, str(key), ".sinf", "config.json"), "w", "utf-8") as file_:
                #     file_.write(json.dumps(midias, ensure_ascii=False, indent=4))
                with open(f"{output_folder}\\{key}\\.sinf\\current_midia.txt", "w") as f:
                    f.write(str(key))
                shutil.copy(os.path.join(script_dir, "launcher_unzipper", "launcher_unzipper.exe"),
                            os.path.join(output_folder, str(key), "Cique aqui para extrair os dados.exe"))
                shutil.copy(Path(script_dir, "copier_rad/Win32/Debug/SinfCopier.exe"), Path(output_folder, f"{key}/.sinf/sinf_copier.exe"))

            for key, value in midias.items():
                for file in value:
                    if not file.endswith("exe"):
                        number = int(file.split(".")[-1])
                        dir_ = f"{output_folder}\\{number}"
                        shutil.copy(f"{script_dir}\\tutorial_renderizado.html",
                                    f"{dir_}\\Instruções.html")

            #ocultar os diretório .sinf
            p = Path(output_folder)
            for entry in p.iterdir():
                if entry.is_dir():
                    p2 = entry / ".sinf"
                    if p2.exists():
                        os.system(f"attrib +h \"{p2}\"")
            f = Figlet()
            print(f.renderText("Atencao"))
            print("\n--------ATENÇÃO---------")
            print("Existe uma pasta oculta de nome \".sinf\" dentro da pasta de cada mídia para gravação. Esta pasta deve ser gravada na mídia também. Caso você tenha costume de trabalhar com o Windows configurado para não mostrar pastas ocultas altere suas configurações antes de gravar as mídias.")
            print("\nGrave cada mídia sem criar nenhuma subpasta. Grave a mídia 1 colocando os arquivos existentes na pasta 1, a mídia 2 com os arquivos existentes na pasta 2, etc.")
            input("Pressione algo para finalizar...")
        else:
            output_folder = Path(output_folder)
            dir_ = output_folder / "1"
            if not dir_.exists():
                dir_.mkdir(parents=True)
            shutil.move(output_folder / "dados.exe", dir_ / "dados.exe")
            shutil.move( output_folder / "dados.7z.001", dir_ / "dados.7z.001")
            shutil.copy(f"{script_dir}\\tutorial_midia_unica.html",
                                    f"{dir_}\\Instruções.html")

            print(f"Grave o conteúdo da pasta \"{dir_.resolve()}\" na mídia.")
            input("Pressione algo para finalizar...")

     
      
