import os
from pathlib import Path

sinftools_dir = os.getenv('SINFTOOLS')

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))

doc_width = 16.5
styles = {
    'p': 'Normal',
    'h1': 'Título 1',
    'h2': 'Título 2',
    'h3': 'Título 3',
    'h4': 'Título 4',
    'h5': 'Título 5',
    'h6': 'Título 6',
    'table': 'ICLR - Tabela',
    'caption': 'legenda'
}

defaults = {
    'p': {
        'indent': 'true',
        'enter': 'true',
        'style': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'ol': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'ul': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'li': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'h1': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'h2': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },

    'h3': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'h4': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'h5': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'h6': {
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'table': {
        'border': 'true',
        'caption': None,
        'caption-label': 'Tabela',
        "caption-col-width": "1",
        'enter': 'true',
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': "center",
        'position': None,
        'style': 'ICLR - Tabela'
    },
    'td': {
        'w': '0.5',
        'font-weight': None,
        'style': 'true',
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'th': {
        'w': '0.5',
        'font-weight': None,
        'font-size': None,
        'style': 'true',
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'text': {
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'alignment': None,
        'position': None
    },
    'figure': {
        'alignment': None,
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'w': '0.5',
        'position': None
    },
    'picture': {
        'alignment': None,
        'font-weight': None,
        'font-size': None,
        'font-name': None,
        'font-color': None,
        'w': '0.5',
        'position': None
    },
    'br':{
        'position': None
    }
}


