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
        "Diretamente no arquivo query.txt": "query",
        "No arquivo categoriesToExport.txt": "categories",
        "No arquivo typesToExport.txt": "types",
    }

    questions = [
        {
            'type': 'list',
            'name': 'filter',
            'message': 'Onde está definido o filtro?',
            'choices': list(options.keys())
        }
    ]

    answers = prompt(questions, style=custom_style)
    return options[answers['filter']]