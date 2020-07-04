import datetime
import os

def formataHorario(horario):
    try:
        return datetime.datetime.fromtimestamp(horario/1000)
    except:
        return None

def eGrupo(row):
    if "g.us" in row['key_remote_jid']:
        return True
    return False

def extrairThumb(con, key_id):
    if not os.path.exists('anexos_whatsapp\\thumbs_extraidos'):
        os.mkdir('anexos_whatsapp\\thumbs_extraidos')
    cursor = con.cursor()
    key_id_str = str(key_id)
    nome_arquivo = key_id_str + ".jpg"
    path_arquivo = 'anexos_whatsapp\\thumbs_extraidos\\' + nome_arquivo
    if os.path.exists(path_arquivo): #se já existe não extrai novamente
        return nome_arquivo
    res = cursor.execute('select thumbnail from message_thumbnails where key_id = ' + "'" + key_id_str + "'").fetchall()
    if res:
        with open(path_arquivo, "wb") as arq:
            arq.write(res[0][0])
        return nome_arquivo
    return None
        