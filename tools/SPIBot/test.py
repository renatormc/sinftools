from pathlib import Path

"""Coloque todos os arquivos txt em uma pasta e execute este script. Antes aponte qual é a pasta"""

replace_items = {
    'da tarde': 'PM',
    'da manhã': 'AM',
    'da noite': 'PM',
    'da madrugada': 'AM'
}

folder = Path(r'C:\temp')  ## Defina aqui a pasta onde se encontram os arquivos txt das conversas

for entry in folder.iterdir():
    if entry.name.endswith(".txt"):
        with entry.open("r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            parts = line.split("-")
            for key, value in replace_items.items():
                parts[0] = parts[0].replace(key, value)
            new_line = "-".join(parts)
            lines[i] = new_line
        with entry.open("w", encoding="utf-8") as f:
            lines = f.writelines(lines)