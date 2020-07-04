import os
import sys
from PyInquirer import style_from_dict, Token, prompt, Separator
sinftools_dir = os.getenv("SINFTOOLS")

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


termo = ""
if len(sys.argv) > 2:
    termo = sys.argv[2]

files = [a.split(".")[0] for a in os.listdir(f'{sinftools_dir}\\scripts')]
choices = []
for file in sorted(files):
    if termo in file:
        choices.append(file)

questions = [
    {
        'type': 'list',
        'message': "Comandos",
        'name': 'action',
        'pageSize': 3,
        'choices': choices
    }
]
res = prompt(questions, style=style)
os.system(res['action'])