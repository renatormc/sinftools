from PyInquirer import style_from_dict, Token, prompt, Separator
from .styles import custom_style_2
import config



def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options

def choose_server():
    questions = [
        {
            'type': 'list',
            'name': 'server',
            'message': 'Selecione um servidor',
            'choices': [key for key in config.servers]
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    return answers['server']




def mark():
    questions = [
        {
            'type': 'list',
            'name': 'role',
            'message': 'Papel?',
            'choices': ['temp', 'final']
        },
        {
            'type': 'input',
            'name': 'name',
            'message': 'Nome do caso:',
            'validate': lambda val: val.strip() != ""
        },
    ]

    answers = prompt(questions, style=custom_style_2)
    answers['name'] = answers['name'].strip()
    return answers


def choose_script():
    questions = [
        {
            'type': 'list',
            'name': 'script',
            'message': 'O que você vai fazer?',
            'choices': list(config.scripts_template.keys())
        },
        {
            'type': 'input',
            'name': 'script_name',
            'message': 'Nome único para o script, sem extensão: '
        },
        {
            'type': 'input',
            'name': 'perito',
            'message': 'Nome do perito: '
        },
    ]

    answers = prompt(questions, style=custom_style_2)

    result = {}
    result['script'] = config.app_dir / f"scripts/{config.scripts_template[answers['script']]['script']}"
    result['process_type'] = config.scripts_template[answers['script']]['process_type']
    result['script_name'] = answers['script_name']
    result['perito'] = answers['perito']
    return result

    