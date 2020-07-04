import settings
from models import *
from database import db_session
from config_manager import config_manager
import sys
from PyInquirer import style_from_dict, Token, prompt, Separator

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def instruct_continue(message):
    print("\n")
    if message:
        print(message)
        print("\n")
    questions = [
        {
            'type': 'list',
            'message': "O que deseja fazer?",
            'name': 'action',
            'pageSize': 3,
            'choices': [
                'Continuar',
                'Cancelar'
            ]
        }
    ]
    res = prompt(questions, style=style)
    if res['action'] == 'Cancelar':
        print("Cancelar")
        sys.exit()
    
    
def show_options_cancel(message, options, cancel_option=False):
    if cancel_option:
        options["Cancelar"] = "cancel"
    questions = [
        {
            'type': 'list',
            'message': message,
            'name': 'action',
            'pageSize': 3,
            'choices': list(options.keys())
        }
    ]
    res = prompt(questions, style=style)
    if cancel_option and options[res['action']] == 'cancel':
        sys.exit()
    return options[res['action']]