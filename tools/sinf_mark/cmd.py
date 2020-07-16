import argparse
from styles import custom_style_2
from PyInquirer import prompt
import markers
from folder_scanner import FolderScanner
import os
from pathlib import Path
import sys
import shutil
import config


parser = argparse.ArgumentParser(
    description='Program that handles makers on folders.')
commands = ['mark', 'delete-markers', 'delete-folders', 'scan', 'find-drives', 'find-cases', 'sinf-mirror', 'find-markers']
parser.add_argument('cmd', nargs='?', type=str, default="mark", help=f"Command")
parser.add_argument('--max-depth', '-m', type=int, default=4, help="Max depth")
parser.add_argument('--drives', '-d', action="store_true",
                    help="Scan all marked drives")
parser.add_argument('--file', '-f', default="C:\\temp\\input_sinf_mirror.txt",  help='Input file to sinf_mirror')
parser.add_argument('--case-name', '-c', help='Case name for sinf_mirror')


args = parser.parse_args()
if args.cmd not in commands:
    print("Comando inválido. Opções disponíveis:\n")
    print("\n".join(commands))
    sys.exit()

if args.cmd == "mark":
    questions = [
        {
            'type': 'list',
            'name': 'type',
            'message': 'Selecione o tipo',
            'choices': ['case', 'disk', 'iped_image_folder', 'delete']
        },
        {
            'type': 'input',
            'name': 'name',
            'message': 'Nome: ',
            'when': lambda answers: answers['type'] in ['case', 'disk']

        },
        {
            'type': 'list',
            'name': 'role',
            'message': 'Papel: ',
            'choices': ['temp', 'final'],
            'when': lambda answers: answers['type'] == 'case'
        },
        {
            'type': 'list',
            'name': 'subtype',
            'message': 'Subtipo: ',
            'choices': ['interno', 'externo'],
            'when': lambda answers: answers['type'] == 'disk'
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    type_ = answers['type']
    if type_ == "case":
        data = {
            "type": answers['type'],
            "name": answers['name'],
            "role": answers['role']
        }
        markers.mark_folder(".", data)
    elif type_ == "disk":
        data = {
            "type": answers['type'],
            "name": answers['name'],
            "subtype": answers['subtype']
        }
        markers.mark_folder(".", data)
    elif type_ in ["iped_image_folder", "delete"]:
        data = {
            "type": answers['type']
        }
        markers.mark_folder(".", data)

elif args.cmd == "delete-markers":
    questions = [
        {
            'type': 'checkbox',
            'name': 'types',
            'message': 'Tipos',
            'choices': [
                {'name': 'case', 'checked': True},
                {'name': 'disk', 'checked': True},
                {'name': 'iped_image_folder', 'checked': True},
            ]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    scanner = FolderScanner()
    scanner.types = answers['types']
    scanner.max_depth = args.max_depth
    scanner.scan_folder(".")
    for folder, markers in scanner.folders.items():
        file_ = Path(folder) / ".sinf_mark.json"
        try:
            file_.unlink()
            print(f"Arquivo \"{file_}\" deletado.")
        except PermissionError:
            print(
                f"Erro de permissão negada ao tentar deletar arquivo \"{file_}\"")

elif args.cmd == "delete-folders":
    scanner = FolderScanner()
    scanner.types = ['delete']
    scanner.max_depth = args.max_depth
    scanner.scan_folder(".")
    if not scanner.folders:
        print("Não foi encontrada nenhuma pasta marcada com o marcador \"delete\"")
        sys.exit()
    print("Foram encontradas as seguintes pastas:")
    # for i, folder in enumerate(scanner.folders.keys()):
    #     print(f"{i + 1}- {folder}")
    questions = [
        {
            'type': 'checkbox',
            'name': 'folders',
            'message': 'Pastas',
            'choices': [{'name': folder, 'checked': True} for folder in scanner.folders.keys()],
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    for folder in answers['folders']:
        shutil.rmtree(folder)

elif args.cmd == "scan":
    questions = [
        {
            'type': 'checkbox',
            'name': 'types',
            'message': 'Tipos',
            'choices': [{'name': t, 'checked': True} for t in config.available_types]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    scanner = FolderScanner()
    scanner.types = answers['types']
    scanner.max_depth = args.max_depth
    if args.drives:
        scanner.scan_drives()
    else:
        scanner.scan_folder(".")
    if scanner.folders:
        questions = [
            {
                'type': 'list',
                'name': 'folder',
                'message': 'Abrir pasta',
                'choices': list(scanner.folders.keys()),
            }
        ]

        answers = prompt(questions, style=custom_style_2)
        os.system(f"explorer \"{answers['folder']}\"")
    else:
        print("Nenhum marcador foi encontrado.")

elif args.cmd == "find-drives":
  
    scanner = FolderScanner()
    scanner.types = ['disk']
    scanner.max_depth = args.max_depth
    scanner.scan_drives()
    print("\nEncontrados:")
    for i, item in enumerate(scanner.folders.items()):
        folder, markers_ = item
        m = markers.get_marker_of_type(markers_, 'disk')
        m['drive'] = folder[:-1]
        print(f"{i+1}- {m}")

elif args.cmd == "find-cases":
  
    scanner = FolderScanner()
    scanner.types = ['case']
    scanner.max_depth = args.max_depth
    if args.drives:
        scanner.scan_drives()
    else:
        scanner.scan_folder(".")
    print("\nEncontrados:")
    for i, item in enumerate(scanner.folders.items()):
        folder, markers_ = item
        m = markers.get_marker_of_type(markers_, 'case')
        m['path'] = folder
        print(f"{i+1}- {m}")

elif args.cmd == "sinf-mirror":
    if not args.case_name:
        print("Não foi informado o nome do caso")
        sys.exit(1)
    scanner = FolderScanner()
    scanner.types = ['case']
    scanner.max_depth = args.max_depth
    scanner.scan_drives()
    sources = []
    dest = None
    for i, item in enumerate(scanner.folders.items()):
        folder, markers_ = item
        m = markers.get_marker_of_type(markers_, 'case')
        if m['name'] == args.case_name:
            if m['role'] == 'temp':
                sources.append(folder)
            elif m['role'] == 'final':
                dest = folder
    if not dest or not Path(dest).exists():
        print("Não foi encontrada a pasta final do caso.")
        sys.exit(1)
    if not sources:
        print("Não foi encontrada nenhuma pasta do tipo temp do caso.")
        sys.exit(1)
    with Path(args.file).open("w", encoding="utf-8") as f:
        f.write(",".join(sources))
        f.write("\n")
        f.write(dest)

elif args.cmd == "find-markers":
    scanner = FolderScanner()
    scanner.types = "*"
    scanner.max_depth = args.max_depth
    scanner.scan_folder(".")
    if scanner.folders:
        questions = [
            {
                'type': 'list',
                'name': 'folder',
                'message': 'Abrir pasta',
                'choices': list(scanner.folders.keys()),
            }
        ]

        answers = prompt(questions, style=custom_style_2)
        os.system(f"explorer \"{answers['folder']}\"")
    else:
        print("Nenhum marcador foi encontrado.")

