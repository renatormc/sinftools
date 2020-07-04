from parsers.xlsx2db.converters import *

possible_sheet_names = {
    'chat': [
        'bate papos', 
        'bate-papos'
        ],
    'contact': [
        'contatos'
        ],
    'call': [
        'registro de chamadas', 
        'chamadas'
        ],
    'sms': [
        'mensagens sms', 
        'mensagens-sms'
        ],
    'image': [
        'imagens'
        ],
    'video': [
        'vídeos', 
        'videos'
        ],
    'audio': [
        'áudios', 
        'audios', 
        'audio', 
        'áudio'
        ],
    'user_account': [
        'contas de usuário', 
        'contas de usuario'
        ]
}

columns = {
    "chat": {
        "id": {
            "possible_names": [
                "#"
            ],
            "converter": integer
        },
        "chat_id": {
            "possible_names": [
                "bate-papo #"
            ],
            "converter": integer
        },
        "chat_name": {
            "possible_names": [
                "identificador"
            ],
            "converter": participant
        },
        "start_time": {
            "possible_names": [
                "hora de início: hora"
            ],
            "converter": timestamp
        },
        "last_activity": {
            "possible_names": [
                "última atividade: hora"
            ],
            "converter": timestamp
        },
        "participants": {
            "possible_names": [
                "Participantes"
            ],
            "converter": participants
        },
        "app": {
            "possible_names": [
                "Origem"
            ],
            "converter": string
        },
        "deleted_chat": {
            "possible_names": [
                "Excluído - Bate-papo"
            ],
            "converter": string
        },
        "from": {
            "possible_names": [
                "De"
            ],
            "converter": participant
        },
        "to": {
            "possible_names": [
                "Para"
            ],
            "converter": string
        },
        "body": {
            "possible_names": [
                "Corpo"
            ],
            "converter": string
        },
        "status": {
            "possible_names": [
                "Status"
            ],
            "converter": string
        },
        "timestamp": {
            "possible_names": [
                "Marcação de tempo: Hora"
            ],
            "converter": timestamp
        },
        "attachment": {
            "possible_names": [
                "Anexo #1"
            ],
            "converter": attachment
        },
        "attachment_details": {
            "possible_names": [
                "Anexo #1 - Detalhes"
            ],
            "converter": string
        },
        "deleted_message": {
            "possible_names": [
                "Excluído - Mensagem instantânea"
            ],
            "converter": string
        },
        "carved": {
            "possible_names": [
                "Vasculhado"
            ],
            "converter": string
        }
    },
    "contact": {
        "name": {
            "possible_names": [
                "Nome"
            ],
            "converter": string
        },
        "entries": {
            "possible_names": [
                "Entradas"
            ],
            "converter": contact_entries
        },
        "source": {
            "possible_names": [
                "Origem"
            ],
            "converter": string
        },
        "deleted": {
            "possible_names": [
                "Excluído"
            ],
            "converter": string
        }
    },
    "call": {
        "parties": {
            "possible_names": [
                "Partes"
            ],
            "converter": parties
        },
        "type": {
            "possible_names": [
                "Tipo de chamada"
            ],
            "converter": string
        },
        "timestamp": {
            "possible_names": [
                "Hora"
            ],
            "converter": timestamp
        },
        "duration": {
            "possible_names": [
                "Duração"
            ],
            "converter": duration
        },
        "deleted": {
            "possible_names": [
                "Excluído"
            ],
            "converter": string
        }
    },
    "sms": {
        "body": {
            "possible_names": [
                "Mensagem"
            ],
            "converter": string
        },
        "parties": {
            "possible_names": [
                "Parte"
            ],
            "converter": parties
        },
        "timestamp": {
            "possible_names": [
                "Hora"
            ],
            "converter": timestamp
        },
        "folder": {
            "possible_names": [
                "Pasta"
            ],
            "converter": string
        },
        "status": {
            "possible_names": [
                "Status"
            ],
            "converter": string
        },
        "deleted": {
            "possible_names": [
                "Excluído"
            ],
            "converter": string
        }
    },
    "file": {
        "id": {
            "possible_names": [
                "#"
            ],
            "converter": integer
        },
        "name": {
            "possible_names": [
                "Nome"
            ],
            "converter": string
        },
        "extracted_path": {
            "possible_names": [
                "Nome"
            ],
            "converter": attachment
        },
        "size": {
            "possible_names": [
                "Tamanho (bytes)"
            ],
            "converter": integer
        },
        "md5": {
            "possible_names": [
                "MD5"
            ],
            "converter": string
        },
        "sha256": {
            "possible_names": [
                "SHA256"
            ],
            "converter": string
        },
        "creation_time": {
            "possible_names": [
                "Criado-Hora",
                "Criado Hora"
            ],
            "converter": timestamp
        },
        "modify_time": {
            "possible_names": [
                "Modificado-Hora",
                "Modificado Hora"
            ],
            "converter": timestamp
        },
        "access_time": {
            "possible_names": [
                "Acessado-Hora",
                "Acessado Hora"
            ],
            "converter": timestamp
        },
        "deleted": {
            "possible_names": [
                "Excluído"
            ],
            "converter": timestamp
        },
    },
    "user_account": {
        "id": {
            "possible_names": [
                "#"
            ],
            "converter": integer
        },
        "name": {
            "possible_names": [
                "Nome da conta"
            ],
            "converter": string
        },
        "username": {
            "possible_names": [
                "Nome de usuário"
            ],
            "converter": string
        },
        "service_type": {
            "possible_names": [
                "Tipo de serviço"
            ],
            "converter": string
        },
        "password": {
            "possible_names": [
                "Senha"
            ],
            "converter": string
        },
        "deleted": {
            "possible_names": [
                "Excluído"
            ],
            "converter": string
        },
    }
}

columns['image'] = columns['file']
columns['audio'] = columns['file']
columns['video'] = columns['file']