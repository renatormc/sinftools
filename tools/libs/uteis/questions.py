
from PyInquirer import style_from_dict, Token, prompt, Separator
import sys

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