from PyInquirer import style_from_dict, Token, prompt, Separator
import os

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def create_dir(value):
    try:
        if not os.path.exists(value):
            os.makedirs(value)
        return True
    except:
        return "Caminho inválido"
       

def get_inputs():
    questions = [
        {
            'type': 'input',
            'name': 'dest_dir',
            'message': 'Diretório de destino:',
            'validate': create_dir
        },
        {
            'type': 'input',
            'name': 'n_cols',
            'message': 'Número de colunas:',
            'default': '3',
            'validate': lambda val: val.isdigit() or 'O número de colunas deve ser um valor inteiro'
        },
        {
            'type': 'input',
            'name': 'n_rows',
            'message': 'Número de linhas:',
            'default': '3',
            'validate': lambda val: val.isdigit() or 'O número de linhas deve ser um valor inteiro'
        },
        {
            'type': 'input',
            'name': 'size',
            'message': 'Tamanho de cada thumbnail (em pixels):',
            'default': '200',
            'validate': lambda val: val.isdigit() or 'O tamanho deve ser um valor inteiro'
        },
        {
            'type': 'list',
            'name': 'extension',
            'message': 'Extensão dos arquivos de thumbs a serem gerados',
            'choices': ['.jpg', '.png', '.bmp']
        }
    ]

    return prompt(questions, style=style)
