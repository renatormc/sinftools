from PyInquirer import style_from_dict, Token, prompt, Separator
from styles import custom_style_2
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