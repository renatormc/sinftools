from pathlib import Path
import os
from styles import custom_style_2
from PyInquirer import prompt
import shutil

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))


questions = [
    {
        'type': 'list',
        'name': 'type',
        'message': 'Tipo',
        'choices': ['UFED Reader', 'Relatório simplificado']
    },
]

answers = prompt(questions, style=custom_style_2)

if answers['type'] == "UFED Reader":
    shutil.copy(app_dir / "UFED READER.vbs", "UFED READER.vbs")
elif answers['type'] == "Relatório simplificado":
    shutil.copy(app_dir / "Relatório simplificado.html", "Relatório simplificado.html")