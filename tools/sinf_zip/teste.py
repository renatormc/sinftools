from sinf.inquirer.inquirer import get_answaers
import os

script_dir =  os.path.dirname(os.path.realpath(__file__))

config_form = {
    "label": "Preencha os dados",
    "items": [
        {
            "type": "combo",
            "name": "dir",
            "label": "Diretório que contém os arquivos a serem comprimidos",
            "list": ["Samsung", "Motorola"],
            "row": 1,
            "stretch": 1
        },
        {
            "type": "combo",
            "name": "type",
            "label": "Tipo de compressão",
            "list": ["7zip", "rar", "sinf"],
            "default": "7zip",
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
            "label": "Calcular has antes de compactar",
            "default": False,
            "row": 3,
            "stretch": 1
        }
    ]
}

a = get_answaers(config_form)
print(a)