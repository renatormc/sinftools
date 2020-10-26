from PyInquirer import style_from_dict, Token, prompt


custom_style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def choose_filter():

    options = {
        "Por categoria": "categories",
        "Por tipo": "types",
        "Por categoria e tipo": "cat_type",
        "Personalizado": "query"
    }

    questions = [
        {
            'type': 'list',
            'name': 'filter',
            'message': 'Escolha o tipo de filtragem:',
            'choices': list(options.keys())
        }
    ]

    answers = prompt(questions, style=custom_style)
    return options[answers['filter']]