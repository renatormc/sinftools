import pandas as pd
import sqlite3
import os
import hashlib
import base64
import codecs
import json
from sinf.report.sqlite_android.auxiliar import *
from sinf.report.funcoes import get_config
from sinf.extractors.readers import *


class SqliteAndroidHandler:
    def __init__(self):
        self.hash_dict = {}
        self.df = None
        self.lista_chats_id = {}
        with codecs.open('.report\config.json', 'r', 'utf-8') as arq:
            self.config_custom = json.load(arq)
        
    def criarDataframesVazios(self):
        columns = ["id", "chat_id", "chat_name", "start_time", "last_activity",
                   "participants", "app", "chat_deleted", "from", "to", "body",
                   "status", "timestamp", "attachment", "attachment_details", "attachment_link", "message_deleted",
                   "quote_attachment", "quote_attachment_link", "quote_attachment_type", "quote_body", "quote_from",
                   "has_quote", "original_source"]
        self.df = pd.DataFrame(columns=columns)
        self.df_contatos = pd.DataFrame(columns=['name', 'entries', 'source', 'deleted', 'original_source'])
        self.df_smss = pd.DataFrame(columns=['body', 'contact', 'timestamp', 'folder', 'deleted', 'original_source'])
        self.df_chamadas = pd.DataFrame(columns=['contact', 'type', 'timestamp', 'duration', 'deleted', 'original_source'])

    def salvar(self):
        config = get_config()
        if not os.path.exists(".report\\save"):
            os.mkdir(".report\\save")
        if config['itens']['bate-papo']:
            self.df.to_pickle(".report\\save\\df_chats")
        if config['itens']['contato']:
            self.df_contatos.to_pickle(".report\\save\\df_contatos")
        if config['itens']['chamada']:
            self.df_chamadas.to_pickle(".report\\save\\df_chamadas")
        if config['itens']['sms']:
            self.df_smss.to_pickle(".report\\save\\df_smss")

    def carregarSalvo(self):
        """Lê o arquivos e carrega na memória"""
        if os.path.exists(".report\\save\\df_chats"):
            self.df = pd.read_pickle(".report\\save\\df_chats")
        if os.path.exists(".report\\save\\df_contatos"):
            self.df_contatos = pd.read_pickle(".report\\save\\df_contatos")
        if os.path.exists(".report\\save\\df_chamadas"):
            self.df_chamadas = pd.read_pickle(".report\\save\\df_chamadas")
        if os.path.exists(".report\\save\\df_smss"):
            self.df_smss = pd.read_pickle(".report\\save\\df_smss")

    def __formatarColunas(self):
        """Na leitura original algumas linhas do dataframe podem ter o tipo do dado errado. Esta função garante que cada coluna tenha o formato necessário"""
        print("Formatando colunas")
        self.df['message_deleted'] = self.df['message_deleted'].apply(lambda x: str(x) if x is not None else '')
        self.df['quote_body'] = self.df['quote_body'].apply(lambda x: str(x) if x is not None else '')
        self.df['quote_attachment_type'] = self.df['quote_attachment_type'].apply(
            lambda x: str(x) if x is not None else '')
        self.df['chat_deleted'] = self.df['chat_deleted'].apply(lambda x: str(x) if x is not None else '')
        self.df['last_activity'] = pd.to_datetime(self.df['last_activity'], errors="coerce")
        self.df['start_time'] = pd.to_datetime(self.df['start_time'], errors="coerce")
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors="coerce")

    def __ordenarPorIdOriginal(self):
        self.df = self.df.sort_values(['chat_id', 'id'], ascending=[True, True])
        self.df = self.df.reset_index(drop=True)

    def getParticipantName(self, identificador):
        try:
            res = self.contacts[self.contacts.jid == identificador]
            if len(res) > 0:
                if res.iloc[0]['given_name'] is not None:
                    return res.iloc[0]['given_name']
                return res.iloc[0]['wa_name']
        except:
            pass
        return None

    def excluirMensagensSistema(self):
        """Exclui as mensagens de sistema, considerando que o código 6 significa mensagem de sistema"""
        self.messages = self.messages[self.messages['status'] != 6]

    def __calcularHashes(self):
        """Percorre recursivamente a pasta de anexos e calcula o hash de cada arquivo para ser comparado depois com o hash gravado no banco de dados. 
        Serve para achar qual é o arquivo relacionado a cada mensagem"""
        self.hash_dict = {}
        print("Calculando hash dos anexos")
        for root, dirs, arquivos in os.walk("anexos_whatsapp"):
            for arq in arquivos:
                m = hashlib.sha256()
                path = os.path.join(root, arq)
                m.update(open(path, 'rb').read())
                self.hash_dict[str(base64.b64encode(m.digest()))[2:-1]] = (root.replace("anexos_whatsapp", ""), arq)

    def __getId(self, row):
        return row['_id']

    def __getChatId(self, row):
        return self.lista_chats_id[row['key_remote_jid']]

    def __getStartTime(self, row):
        res = self.chat_list[self.chat_list.key_remote_jid == row.key_remote_jid]
        if len(res) > 0:
            return formataHorario(res.iloc[0]['creation'])

    def __getLastActivity(self, row):
        res = self.messages[self.messages.key_remote_jid == row.key_remote_jid].sort_values('timestamp',
                                                                                            ascending=False)
        return formataHorario(res.iloc[0]['timestamp'])

    def __getTimestamp(self, row):
        return formataHorario(row['timestamp'])

    def __getChatName(self, row):
        if eGrupo(row):
            res = self.chat_list[self.chat_list.key_remote_jid == row.key_remote_jid]
            if len(res) > 0:
                aux = [row.key_remote_jid if row.key_remote_jid is not None else '',
                       res.iloc[0]['subject'] if res.iloc[0]['subject'] is not None else '']
                return " ".join(aux)
        else:
            part_name = self.getParticipantName(row.key_remote_jid)
            aux = [row.key_remote_jid if row.key_remote_jid is not None else '',
                   part_name if part_name is not None else '']
            return " ".join(aux)

    def __getParticipants(self, row):
        df_filtrado = self.group_participants[(self.group_participants['gjid'] == row['key_remote_jid']) & (
            self.group_participants['jid'].str.contains('@'))]
        parts = []
        for i, row in df_filtrado.iterrows():
            part_name = self.getParticipantName(row.jid)
            aux = [row.jid if row.jid is not None else '', part_name if part_name is not None else '']
            parts.append(" ".join(aux))
        parts.append(self.config_custom['identificador_usuario_whatsapp_sqlite'] + " " + self.config_custom[
            'nome_usuario_whatsapp_sqlite'])
        return "\n".join(parts)

    def __getApp(self, row):
        return 'WhatsApp'

    def __getChatDeleted(self, row):
        ''

    def __getFrom(self, row):
        if eGrupo(row):
            if row['key_from_me'] == 0:
                part_name = self.getParticipantName(row.remote_resource)
                aux = [row.remote_resource if (
                            row.remote_resource is not None or str(row.key_remote_resource) == '') else '',
                       part_name if part_name is not None else '']
                return " ".join(aux)
            if row['key_from_me'] == 1 and (row['remote_resource'] is None or str(row['remote_resource']) == ''):
                return self.config_custom['identificador_usuario_whatsapp_sqlite'] + " " + self.config_custom[
                    'nome_usuario_whatsapp_sqlite']
            else:
                return ''
        else:
            if row['key_from_me'] == 0:
                part_name = self.getParticipantName(row.key_remote_jid)
                aux = [row.key_remote_jid if row.key_remote_jid is not None else '',
                       part_name if part_name is not None else '']
                return " ".join(aux)
            elif row['key_from_me'] == 1:
                return self.config_custom['identificador_usuario_whatsapp_sqlite'] + " " + self.config_custom[
                    'nome_usuario_whatsapp_sqlite']

    def __getTo(self, row):
        return ''

    def __getBody(self, row):
        return row['data'] if row['data'] is not None else ''

    def __getStatus(self, row):
        return ''

    def __getTimeStamp(self, row):
        return row['timestamp']

    def __getAttachment(self, row):
        arquivo_existe = row['media_hash'] in self.hash_dict
        if arquivo_existe:
            return self.hash_dict[row['media_hash']][1]
        arquivo_extraido = extrairThumb(self.con_msgstore, row['key_id'])
        if arquivo_extraido:
            return arquivo_extraido
        if row['media_name'] is not None:
            return row['media_name'] + " (Mídia indisponível)"
        if row['media_hash'] is not None:
            return 'Anexo desconhecido (Mídia indisponível)'
        return ''

    def __getAttachmentLink(self, row):
        if row['media_hash'] in self.hash_dict:
            res = self.hash_dict[row['media_hash']]
            return "/".join(["anexos_whatsapp", res[0].replace("\\", "/"), res[1].replace("\\", "/")])
        arquivo_extraido = extrairThumb(self.con_msgstore, row['key_id'])
        if arquivo_extraido:
            return "/".join(["anexos_whatsapp", "thumbs_extraidos", arquivo_extraido])
        return ''

    def __getAttachmentDetails(self, row):
        return row['media_caption'] if row['media_caption'] is not None else ''

    def __getMessageDeleted(self, row):
        ''

    def __getQuoteAttachement(self, row):
        res = self.messages_quotes[self.messages_quotes._id == row['quoted_row_id']]
        if len(res) > 0:
            row_ = res.iloc[0]
            return self.__getAttachment(row_)
        return ''

    def __getQuoteAttachmentLink(self, row):
        res = self.messages_quotes[self.messages_quotes._id == row['quoted_row_id']]
        if len(res) > 0:
            row_ = res.iloc[0]
            return self.__getAttachmentLink(row_)
        return ''

    def __getQuoteAttachmentType(self, row):
        ''

    def __getQuoteBody(self, row):
        res = self.messages_quotes[self.messages_quotes._id == row['quoted_row_id']]
        if len(res) > 0:
            row_ = res.iloc[0]
            return row_['data']
        return ''

    def __getQuoteFrom(self, row):
        res = self.messages_quotes[self.messages_quotes._id == row['quoted_row_id']]
        if len(res) > 0:
            row_ = res.iloc[0]
            return self.__getFrom(row_)
        return ''

    def __getHasQuote(self, row):
        if row['quoted_row_id'] != 0:
            return True
        return False

    def carregarSqliteParaDataFrame(self):
        """Pega as tabelas dos sqlite e joga cada uma em um dataframe. Todo trabalho depois de parsing é feito no dataframe e não no banco de dados"""
        if not os.path.exists(".report\\msgstore.db"):
            print("Não foi encontrado o arquivo '.report\\msgstore.db'")
            exit()
        self.con_msgstore = sqlite3.connect(".report\\msgstore.db")
        self.messages = pd.read_sql_query("SELECT * from messages", self.con_msgstore)

        self.chat_list = pd.read_sql_query("SELECT * from chat_list", self.con_msgstore)

        self.group_participants = pd.read_sql_query("SELECT * from group_participants", self.con_msgstore)

        self.messages_quotes = pd.read_sql_query("SELECT * from messages_quotes", self.con_msgstore)
        try:
            con_wa = sqlite3.connect(".report\\wa.db")
            self.contacts = pd.read_sql_query("SELECT * from wa_contacts", con_wa)
        except:
            self.contacts = None

    def lerSqliteWhatsapp(self):
        """Converte o dataframe bruto, aquele que é apenas uma cópia dos dados do sqlite, para o dataframe no formato necessário"""
        self.lista_chats_id = {grupo: i for i, grupo in
                               enumerate(self.messages.groupby('key_remote_jid').groups.keys())}
        self.__calcularHashes()
        print("Montando data-frame")
        # Adiciona linha por linha pegando do dataframe com os dados brutos e passando cada linha pelas funções que retornarão os dados formatados que serão salvos no dataframe padronizado
        qtd = self.messages.shape[0]
        for i, row in self.messages.iterrows():
            # print(f"{i+1} de {qtd}")
            data = {
                "id": self.__getId(row),
                "chat_id": self.__getChatId(row),
                "chat_name": self.__getChatName(row),
                "start_time": self.__getStartTime(row),
                "last_activity": self.__getLastActivity(row),
                "participants": self.__getParticipants(row),
                "app": self.__getApp(row),
                "chat_deleted": self.__getChatDeleted(row),
                "from": self.__getFrom(row),
                "to": self.__getTo(row),
                "body": self.__getBody(row),
                "status": self.__getStatus(row),
                "timestamp": self.__getTimestamp(row),
                "attachment": self.__getAttachment(row),
                "attachment_details": self.__getAttachmentDetails(row),
                "message_deleted": self.__getMessageDeleted(row),
                "attachment_link": self.__getAttachmentLink(row),
                "quote_attachment": self.__getQuoteAttachement(row),
                "quote_attachment_link": self.__getQuoteAttachmentLink(row),
                "quote_attachment_type": self.__getQuoteAttachmentType(row),
                "quote_body": self.__getQuoteBody(row),
                "quote_from": self.__getQuoteFrom(row),
                "has_quote": self.__getHasQuote(row),
                "original_source": "sqlite"
            }
            df2 = pd.DataFrame([data])
            self.df = self.df.append(df2, ignore_index=True)
        self.__formatarColunas()
        self.__ordenarPorIdOriginal()  # para manter a ordem que o aplicativo do banco de dados do Android mantinha

    def lerContatos(self):
        if os.path.exists(".report\\contacts2.db"):
            contacts = getContacts_1(".report\\contacts2.db")
            for contact in contacts:
                reg = pd.DataFrame({'name': contact.name, 'entries': contact.entries, 'source': contact.source,
                                    'deleted': contact.deleted, 'original_srouce': 'sqlite'})
                self.df_contatos = self.df_contatos.append(reg, ignore_index=True)


    def lerSmss(self):
        if os.path.exists(".report\\mmssms.db"):
            smss = getSmss_1(".report\\mmssms.db")
            for sms in smss:
                reg = pd.DataFrame([{"body": sms.body, "contact": sms.contact, "timestamp": sms.time, "folder": sms.type,
                                    "deleted": sms.deleted,'original_srouce': 'sqlite'}])
                self.df_smss = self.df_smss.append(reg, ignore_index=True)


    def lerChamadas(self):
        if os.path.exists(".report\\logs.db"):
            calls = getCalls_1(".report\\logs.db")
            for call in calls:
                reg = pd.DataFrame([{"contact": call.contact, "type": call.type, "timestamp": call.timestamp, "duration": call.duration, "deleted": call.deleted, 'original_srouce': 'sqlite'}])
                self.df_chamadas = self.df_chamadas.append(reg, ignore_index=True)


if __name__ == "__main__":
    os.chdir(r'C:\Users\renato\Desktop\sqlite')
    hd = SqliteAndroidHandler()
    hd.lerContatos()
    hd.lerChamadas()
