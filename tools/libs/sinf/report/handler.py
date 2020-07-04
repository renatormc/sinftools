# -*- coding: utf-8 -*-
import codecs

import pandas as pd

pd.options.mode.chained_assignment = None
pd.set_option('display.max_colwidth', -1)
import pickle
from sinf.report.auxiliar import *
import json
import datetime
from sinf.report import renderizador
# from sinf.report.config import config
from sinf.report.auxiliar import copyanything
from sinf.report.funcoes import findXLSX, copiaArquivosNecessarios, countAudios, countImages, countVideos
from sinf.report.format_converter import FormatConverter
import pathlib

script_dir = os.path.dirname(os.path.realpath(__file__))


def getVersoesDisponiveis():
    return [s.replace('.json', '') for s in os.listdir("{}\\config_files".format(script_dir))]


class Handler:
    def __init__(self):
        # self.config = config
        self.config_custom = self.lerConfigFile()
        # if self.config_custom:
        #     self.config['dono_celular'] = self.config_custom['dono_celular']
        #     self.config['mapa_colunas'] = self.config_custom['mapa_colunas']
        #     self.config['mapa_colunas_smss'] = self.config_custom['mapa_colunas_smss']
        #     self.config['mapa_colunas_contatos'] = self.config_custom['mapa_colunas_contatos']
        #     self.config['mapa_colunas_chamadas'] = self.config_custom['mapa_colunas_chamadas']
        #     self.config['mapa_colunas_imagens'] = self.config_custom['mapa_colunas_imagens']
        #     self.config['mapa_colunas_videos'] = self.config_custom['mapa_colunas_videos']
        #     self.config['linha_cabecalho'] = int(self.config_custom['linha_cabecalho'])
        # self.arquivo = self.config_custom['arquivo']
        self.chats_gerados = None
        self.rend = renderizador.Renderizador()
        self.rend.setTemplatesFolder('{}\\templates'.format(script_dir))
        self.ultima_acao = None
        self.df = None
        self.df_smss = None
        self.df_contatos = None
        self.df_chamadas = None
        self.df_imagens = None
        self.df_audios = None
        self.df_videos = None
        self.processado = False
        self.dataframe_gerado = False
        self.df_converted_files = pd.DataFrame(columns=['old_filename', 'new_filename'])
        self.n_renderizacoes = 0
        self.ultima_modificacao = ""

    def lerConfigFile(self):
        if not os.path.exists('.report\config.json'):
            print("Não foi encontrado o arquivo \".report\config.json\"")
            return
        with codecs.open('.report\config.json', 'r', 'utf-8') as arq:
            dadosjson = json.load(arq)
        return dadosjson

    # def setUsuarioWhatsapp(self, usuario):
    #     self.config['dono_celular']['WhatsApp'] = usuario
    #
    # def setUsuarioFacebook(self, usuario):
    #     self.config['dono_celular']['Facebook messenger'] = usuario

    def mudarVersaoDoUfed(self):
        print("\nEscolha uma das opções disponíveis abaixo.")
        versoes = getVersoesDisponiveis()
        for i, versao in enumerate(versoes):
            print("  {}- {}".format(i + 1, versao))
        while True:
            op = input("\nop: ")
            if not op.isdigit() or int(op) > len(versoes):
                print("opcão incorreta.")
            else:
                arquivo = "{}\\config_files\\{}.json".format(script_dir, versoes[int(op) - 1])
                break

        with codecs.open(".report\\config.json", "r", "utf-8") as f:
            data_to = json.load(f)
        with codecs.open(arquivo, "r", "utf-8") as f:
            data_from = json.load(f)

        data_to["mapa_colunas"] = data_from['mapa_colunas']
        data_to["planilhas"] = data_from['planilhas']
        data_to["mapa_colunas_contatos"] = data_from['mapa_colunas_contatos']
        data_to["mapa_colunas_chamadas"] = data_from['mapa_colunas_chamadas']
        data_to["mapa_colunas_smss"] = data_from['mapa_colunas_smss']
        data_to["linha_cabecalho"] = data_from['linha_cabecalho']

        with codecs.open(".report\\config.json", "w", "utf-8") as f:
            f.write(json.dumps(data_to, ensure_ascii=False, indent=2))
        print("Versão alterada.")

    def lerDadosHandlerSalvo(self):
        if not os.path.exists(".report\\save\\chat_handler_data"):
            return None

        with open(".report\\save\\chat_handler_data", 'rb') as f:
            obj = pickle.load(f)
        self.chats_gerados = obj['chats_gerados']
        self.ultima_acao = obj['ultima_acao']
        self.processado = obj['processado']
        self.dataframe_gerado = obj['dataframe_gerado']
        self.n_renderizacoes = obj['n_renderizacoes']
        self.horario_ultimo_salvar = obj['horario_ultimo_salvar']
        return True

    def carregarSalvo(self):
        res = self.lerDadosHandlerSalvo()
        if not res and self.config_custom['fonte_dados'] != 'sqlite':
            res_ = self.carregar()
            if not res_:
                return None
        if self.config_custom['itens']['bate-papo']:
            if os.path.exists(".report\\save\\df_chats"):
                self.df = pd.read_pickle(".report\\save\\df_chats")
                self.dataframe_gerado = True
            else:
                print(
                    "Não foi encontrado o arquivo \".report\\save\\df_chats\". Provavelmente você está pulando etapa.")
                return
        if self.config_custom['itens']['sms']:
            if os.path.exists(".report\\save\\df_smss"):
                self.df_smss = pd.read_pickle(".report\\save\\df_smss")
            else:
                print("Não foi encontrado o arquivo \".report\\save\\df_smss\". Provavelmente você está pulando etapa.")
                return
        if self.config_custom['itens']['contato']:
            if os.path.exists(".report\\save\\df_contatos"):
                self.df_contatos = pd.read_pickle(".report\\save\\df_contatos")
            else:
                print(
                    "Não foi encontrado o arquivo \".report\\save\\df_contatos\". Provavelmente você está pulando etapa.")
                return
        if self.config_custom['itens']['chamada']:
            if os.path.exists(".report\\save\\df_chamadas"):
                self.df_chamadas = pd.read_pickle(".report\\save\\df_chamadas")
            else:
                print(
                    "Não foi encontrado o arquivo \".report\\save\\df_chamadas\". Provavelmente você está pulando etapa.")
                return
        if self.config_custom['itens']['imagem']:
            if os.path.exists(".report\\save\\df_imagens"):
                self.df_imagens = pd.read_pickle(".report\\save\\df_imagens")
            else:
                print(
                    "Não foi encontrado o arquivo \".report\\save\\df_imagens\". Provavelmente você está pulando etapa.")
                return
        if self.config_custom['itens']['audio']:
            if os.path.exists(".report\\save\\df_audios"):
                self.df_audios = pd.read_pickle(".report\\save\\df_audios")
            else:
                print(
                    "Não foi encontrado o arquivo \".report\\save\\df_audios\". Provavelmente você está pulando etapa.")
                return
        if self.config_custom['itens']['video']:
            if os.path.exists(".report\\save\\df_videos"):
                self.df_videos = pd.read_pickle(".report\\save\\df_videos")
            else:
                print(
                    "Não foi encontrado o arquivo \".report\\save\\df_videos\". Provavelmente você está pulando etapa.")
                return
        if os.path.exists(".report\\save\\df_converted_files"):
            self.df_converted_files = pd.read_pickle(".report\\save\\df_converted_files")
        

        print("Dados carregados.")
        try:
            print("Última modificação: " + self.horario_ultimo_salvar.strftime("%d/%m/%Y %H:%M:%S"))
            if self.ultima_acao:
                print("Última ação: " + self.ultima_acao)
        except:
            pass
        return True

    def registryFileConverted(self, old_filename, new_filename):
        df = pd.DataFrame({"old_filename": [old_filename], "new_filename": [new_filename]})
        self.df_converted_files = pd.concat([self.df_converted_files, df])

    def consultFileConverted(self, old_filename):
        df = self.df_converted_files[self.df_converted_files['old_filename']==old_filename]
        if df.shape[0] > 0:
            return (True, df.iloc[0]['new_filename'])
        else:
            return (False, "")

    def salvar(self):
        if not os.path.exists(".report\\save"):
            os.mkdir(".report\\save")
        dados = {
            'chats_gerados': self.chats_gerados,
            'ultima_acao': self.ultima_acao,
            'horario_ultimo_salvar': datetime.datetime.now(),
            'processado': self.processado,
            'dataframe_gerado': self.dataframe_gerado,
            'n_renderizacoes': self.n_renderizacoes
        }
        with open(".report\\save\\chat_handler_data", 'wb') as f:
            pickle.dump(dados, f, pickle.HIGHEST_PROTOCOL)
        if self.df is not None:
            self.df.to_pickle(".report\\save\\df_chats")
        if self.df_smss is not None:
            self.df_smss.to_pickle(".report\\save\\df_smss")
        if self.df_contatos is not None:
            self.df_contatos.to_pickle(".report\\save\\df_contatos")
        if self.df_chamadas is not None:
            self.df_chamadas.to_pickle(".report\\save\\df_chamadas")
        if self.df_imagens is not None:
            self.df_imagens.to_pickle(".report\\save\\df_imagens")
        if self.df_audios is not None:
            self.df_audios.to_pickle(".report\\save\\df_audios")
        if self.df_videos is not None:
            self.df_videos.to_pickle(".report\\save\\df_videos")
        if self.df_converted_files is not None:
            self.df_converted_files.to_pickle(".report\\save\\df_converted_files")

    def carregar(self, arquivo=None):
        self.arquivo = arquivo
        bate_papos = self.config_custom['itens']['bate-papo']
        smss = self.config_custom['itens']['sms']
        contatos = self.config_custom['itens']['contato']
        chamadas = self.config_custom['itens']['chamada']
        video = self.config_custom['itens']['video']
        imagem = self.config_custom['itens']['imagem']
        audio = self.config_custom['itens']['audio']
        if not arquivo and self.config_custom['fonte_dados'] == 'excel':
            res = findXLSX()
            if not res:  # não voi encontrada a planilha
                return
            self.arquivo = res
        dono_celular = self.config_custom["dono_celular"]
        print('\nCarregando dados da planilha')
        aux = loadFromExcel(self.arquivo, planilha=self.lerConfigFile()['planilhas']['bate_papos'],
                            config_custom=self.config_custom,
                            linha_cabecalho=self.config_custom["linha_cabecalho"], metodo=2,
                            bate_papos=bate_papos, smss=smss, chamadas=chamadas, contatos=contatos, imagens=imagem,
                            videos=video, audios=audio)
        self.df = aux['bate_papos']
        self.df_smss = aux['smss']
        self.df_contatos = aux['contatos']
        self.df_chamadas = aux['chamadas']
        self.df_imagens = aux['imagens']
        self.df_videos = aux['videos']
        self.df_audios = aux['audios']
        self.df_converted_files = pd.DataFrame(columns=['old_filename', 'new_filename'])

        erros = []
        if self.config_custom['itens']['bate-papo']:
            colunas_ausentes = self.confereColunas()
            if colunas_ausentes:
                erros.append("Não foram encontradas na planilha de bate-papos as colunas {}.".format(colunas_ausentes))
        if self.config_custom['itens']['sms']:
            colunas_ausentes = self.confereColunasSmss()
            if colunas_ausentes:
                erros.append(
                    "Não foram encontradas na planilha de mensagens SMS as colunas {}.".format(colunas_ausentes))
        if self.config_custom['itens']['contato']:
            colunas_ausentes = self.confereColunasContatos()
            if colunas_ausentes:
                erros.append("Não foram encontradas na planilha de contatos as colunas {}.".format(colunas_ausentes))
        if self.config_custom['itens']['chamada']:
            colunas_ausentes = self.confereColunasChamadas()
            if colunas_ausentes:
                erros.append(
                    "Não foram encontradas na planilha de Registro de chamadas as colunas {}.".format(colunas_ausentes))
        if self.config_custom['itens']['imagem']:
            colunas_ausentes = self.confereColunasImagens()
            if colunas_ausentes:
                erros.append(
                    "Não foram encontradas na planilha de Imagens as colunas {}.".format(colunas_ausentes))
        if self.config_custom['itens']['audio']:
            colunas_ausentes = self.confereColunasAudios()
            if colunas_ausentes:
                erros.append(
                    "Não foram encontradas na planilha de Audios as colunas {}.".format(colunas_ausentes))
        if self.config_custom['itens']['video']:
            colunas_ausentes = self.confereColunasVideos()
            if colunas_ausentes:
                erros.append(
                    "Não foram encontradas na planilha de Vídeos as colunas {}.".format(colunas_ausentes))
        if erros:
            print('\nERROS ENCONTRADOS:')
            for i, erro in enumerate(erros):
                print("{}- {}".format(i + 1, erro))
            print('\nConfira no arquivo ".report\\config.json" e o arquivo Excel.')
            print('\nPossíveis problemas:')
            print('-Os mapas de colunas estão errados')
            print('-As colunas que não foram encontradas não existem no arquivo Excel')
            print('-A linha de cabeçalho definida no arquivo "config.json" está errada')
        else:
            self.__deletarColunas()
            self.__organizarHorarios()
            self.dataframe_gerado = True
        return True

    def confereColunas(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas'].values():
            if coluna not in self.df.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def confereColunasSmss(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas_smss'].values():
            if coluna not in self.df_smss.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def confereColunasContatos(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas_contatos'].values():
            if coluna not in self.df_contatos.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def confereColunasChamadas(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas_chamadas'].values():
            if coluna not in self.df_chamadas.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def confereColunasImagens(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas_imagens'].values():

            if coluna not in self.df_imagens.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def confereColunasAudios(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas_audios'].values():

            if coluna not in self.df_audios.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def confereColunasVideos(self):
        colunas_ausentes = []
        for coluna in self.config_custom['mapa_colunas_videos'].values():
            if coluna not in self.df_videos.keys():
                colunas_ausentes.append(coluna)
        return colunas_ausentes

    def __deletarColunas(self):
        # %%Deleta Colunas
        if self.config_custom['itens']['bate-papo']:
            print('Excluindo colunas desnecessárias dos bate-papos')
            inverted_map = {x: y for y, x in self.config_custom['mapa_colunas'].items()}
            self.df = self.df.rename(columns=inverted_map)

            colunas = ['id',
                       'chat_id',
                       'chat_name',
                       'start_time',
                       'last_activity',
                       'participants',
                       'app',
                       'chat_deleted',
                       'from',
                       'body',
                       'timestamp',
                       'attachment',
                       'attachment_details',
                       'message_deleted',
                       'attachment_link',
                       'carved']
            self.df = self.df[colunas]

        self.ultima_acao = 'deletar colunas'

    def deletarColunasImagens(self):
        if self.df_imagens is not None:
            print('Excluindo colunas desnecessárias das imagens')
            inverted_map = {x: y for y, x in self.config_custom["mapa_colunas_imagens"].items()}
            self.df_imagens = self.df_imagens.rename(columns=inverted_map)
            colunas = list(self.config_custom["mapa_colunas_imagens"].keys())
            colunas.append("link")
            self.df_imagens = self.df_imagens[colunas]

    def deletarColunasAudios(self):
        if self.df_audios is not None:
            print('Excluindo colunas desnecessárias dos audios')
            inverted_map = {x: y for y, x in self.config_custom["mapa_colunas_audios"].items()}
            self.df_audios = self.df_audios.rename(columns=inverted_map)
            colunas = list(self.config_custom["mapa_colunas_audios"].keys())
            colunas.append("link")
            self.df_audios = self.df_audios[colunas]

    def deletarColunasVideos(self):
        if self.df_videos is not None:
            print('Excluindo colunas desnecessárias dos videos')
            inverted_map = {x: y for y, x in self.config_custom["mapa_colunas_videos"].items()}
            self.df_videos = self.df_videos.rename(columns=inverted_map)
            colunas = list(self.config_custom["mapa_colunas_videos"].keys())
            colunas.append("link")
            self.df_videos = self.df_videos[colunas]

    def deletarColunasSmss(self):
        # %%Deleta Colunas sms
        if self.df_smss is not None:
            try:
                print('Excluindo colunas desnecessárias das mensagens sms')
                inverted_map = {x: y for y, x in self.config_custom['mapa_colunas_smss'].items()}
                self.df_smss = self.df_smss.rename(columns=inverted_map)

                colunas = list(inverted_map.values())
                self.df_smss = self.df_smss[colunas]
                self.ultima_acao = 'deletar colunas das mensagens sms'
            except:
                print("Erro ao tentar deletar colunas sms, porém não afeta o resultado.")

    def deletarColunasContatos(self):
        # %%Deleta Colunas contatos
        if self.df_contatos is not None:
            try:
                print('Excluindo colunas desnecessárias da lista de contatos')
                inverted_map = {x: y for y, x in self.config_custom["mapa_colunas_contatos"].items()}
                self.df_contatos = self.df_contatos.rename(columns=inverted_map)

                colunas = list(inverted_map.values())
                self.df_contatos = self.df_contatos[colunas]
                self.ultima_acao = 'deletar colunas da lista de contatos'
            except:
                print("Erro ao tentar deletar colunas contatos, porém não afeta o resultado.")

    def deletarColunasChamadas(self):
        # %%Deleta Colunas chamadas
        if self.df_chamadas is not None:
            try:
                print('Excluindo colunas desnecessárias dos registros de chamadas')
                inverted_map = {x: y for y, x in self.config_custom["mapa_colunas_chamadas"].items()}
                self.df_chamadas = self.df_chamadas.rename(columns=inverted_map)

                colunas = list(inverted_map.values())
                self.df_chamadas = self.df_chamadas[colunas]
                self.ultima_acao = 'deletar colunas dos registros de chamadas'
            except:
                print("Erro ao tentar deletar colunas chamadas, porém não afeta o resultado.")

    def traduzirSmss(self):
        if self.df_smss is not None:
            def traduzir(value):
                try:
                    retorno = str(value).replace('Inbox', 'Recebido')
                    retorno = retorno.replace('Sent', 'Enviado')
                except:
                    retorno = value
                return retorno

            self.df_smss['folder'] = self.df_smss['folder'].apply(traduzir)

    def __organizarHorarios(self):
        # %% Organizar horários
        if self.config_custom['itens']['bate-papo']:
            print('Organizando horários dos bate-papos')
            self.df['start_time'] = self.df['start_time'].replace(self.config_custom["formato_hora"]['formato'],
                                                                  self.config_custom["formato_hora"]['substituto'], regex=True)
            self.df['start_time'] = pd.to_datetime(self.df['start_time'], errors='coerce')
            self.df['last_activity'] = self.df['last_activity'].replace(self.config_custom["formato_hora"]['formato'],
                                                                        self.config_custom["formato_hora"]['substituto'],
                                                                        regex=True)
            self.df['last_activity'] = pd.to_datetime(self.df['last_activity'], errors='coerce')
            self.df['timestamp'] = self.df['timestamp'].replace(self.config_custom["formato_hora"]['formato'],
                                                                self.config_custom["formato_hora"]['substituto'], regex=True)
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], errors='coerce')
            self.ultima_acao = 'organizar horários'

    def ordenarDataFrame(self):
        # %% Ordenar data frame
        if self.config_custom['itens']['bate-papo']:
            self.df = self.df.sort_values(by=['app', 'last_activity'], ascending=[True, False])

            # %% converter  para string
            self.df['body'] = self.df['body'].dropna()
            self.df['body'] = self.df['body'].apply(str)
            self.df['chat_name'] = self.df['chat_name'].apply(str)
            self.df['from'] = self.df['from'].apply(str)
            self.ultima_acao = 'ordenar data-frame'

    def acrescentarColunasQuote(self):
        self.df["quote_attachment"] = ""
        self.df["quote_attachment_link"] = ""
        self.df["quote_attachment_type"] = ""
        self.df["quote_body"] = ""
        self.df["quote_from"] = ""
        self.df["has_quote"] = ""

    def acrescentarColunas(self):
        # %%Acrescenta colunas
        if self.config_custom['itens']['bate-papo']:
            print('Criando colunas extras nos bate-papos')
            self.df['formatted_chat_name'] = self.df['chat_name']
            self.df['formatted_from'] = self.df['from']
            self.df['formatted_chat_name'][self.df['app'] == 'WhatsApp'] = self.df['chat_name'][
                self.df['app'] == 'WhatsApp'].apply(formataId, args=('WhatsApp',))
            self.df['formatted_from'][self.df['app'] == 'WhatsApp'] = self.df['from'][
                self.df['app'] == 'WhatsApp'].apply(formataId, args=('WhatsApp',))
            self.df['formatted_chat_name'][self.df['app'] == 'Facebook messenger'] = self.df['chat_name'][
                self.df['app'] == 'Facebook messenger'].apply(formataId, args=('Facebook messenger',))
            self.df['formatted_from'][self.df['app'] == 'Facebook messenger'] = self.df['from'][
                self.df['app'] == 'Facebook messenger'].apply(formataId, args=('Facebook messenger',))
            self.df['formatted_chat_name'][self.df['formatted_chat_name'] == ''] = 'Desconhecido'
            self.df['formatted_quote_from'] = self.df['quote_from']
            self.df['formatted_quote_from'][self.df['app'] == 'WhatsApp'] = self.df['quote_from'][
                self.df['app'] == 'WhatsApp'].apply(formataId, args=('WhatsApp',))

            self.df['from'][self.df['from'] == ''] = 'Desconhecido'
            df2 = self.df[self.df['formatted_chat_name'] == 'Desconhecido']
            self.df['user_message'] = False
            self.df['user_message'] = self.df['from'].apply(eDono,
                                                            args=(self.config_custom["dono_celular"],))
            self.df['avatar_chat'] = ''
            self.df['avatar_from'] = ''
            if len(self.df[self.df.app == "WhatsApp"]) > 0:
                tipo_telefone = self.config_custom['tipo_telefone']
                self.df['avatar_from'][self.df['app'] == 'WhatsApp'] = self.df[self.df['app'] == 'WhatsApp'].apply(
                    getAvatarWhatsapp, axis=1, args=('from',tipo_telefone,))
                self.df['avatar_chat'][self.df['app'] == 'WhatsApp'] = self.df[self.df['app'] == 'WhatsApp'].apply(
                    getAvatarWhatsapp, axis=1, args=('chat_name', tipo_telefone,))
            self.df['tagged'] = False
            self.df['tagged2'] = False
            self.df['tagged_word'] = False
            self.df['midia_converted'] = False
            self.df['attachment_link_before_conversion'] = ""
            self.df['page'] = 0
            self.df['original_source'] = 'excel'
            self.df.chat_id = self.df.chat_id.apply(int)
            self.ultima_acao = 'acrescentar colunas'

    def acrescentarColunasImagens(self):
        if self.config_custom['itens']['imagem']:
            self.df_imagens['tagged'] = False
            self.df_imagens['tagged2'] = False
            self.df_imagens['tagged_word'] = False
            self.df_imagens['midia_converted'] = False
            self.df_imagens['link_before_conversion'] = ""
            self.df_imagens['renderizar'] = True

    def acrescentarColunasAudios(self):
        if self.config_custom['itens']['audio']:
            self.df_audios['tagged'] = False
            self.df_audios['tagged2'] = False
            self.df_audios['tagged_word'] = False
            self.df_audios['midia_converted'] = False
            self.df_audios['link_before_conversion'] = ""
            self.df_audios['renderizar'] = True

    def acrescentarColunasVideos(self):
        if self.config_custom['itens']['video']:
            self.df_videos['tagged'] = False
            self.df_videos['tagged2'] = False
            self.df_videos['tagged_word'] = False
            self.df_videos['midia_converted'] = False
            self.df_videos['link_before_conversion'] = ""
            self.df_videos['renderizar'] = True

    def modificarIdentificadorWhatsapp(self):
        if self.config_custom['itens']['bate-papo']:
            print('Modificando identificador das conversas do WhatsApp')

            def wModificar(row):
                participantes = [part.strip() for part in str(row['participants']).split("\n") if part.strip() != '']
                if len(participantes) > 2:
                    return row['formatted_chat_name']
                if len(participantes) == 2:
                    if self.config_custom["dono_celular"]['WhatsApp'] in participantes[0]:
                        return formataIdWhatsapp(participantes[1])
                    elif self.config_custom["dono_celular"]['WhatsApp'] in participantes[1]:
                        return formataIdWhatsapp(participantes[0])
                    else:
                        return row['formatted_chat_name']
                if len(participantes) == 1:
                    if self.config_custom["dono_celular"]['WhatsApp'] not in participantes[0]:
                        return formataIdWhatsapp(participantes[0])
                return row['formatted_chat_name']

            if self.config_custom["dono_celular"]['WhatsApp'].strip() != '':
                self.df['formatted_chat_name'][self.df['app'] == 'WhatsApp'] = self.df[
                    self.df['app'] == 'WhatsApp'].apply(wModificar, axis=1)
            self.ultima_acao = 'modificar identificador do WhatsApp'

    def modificarIdentificadorFacebook(self):
        if self.config_custom['itens']['bate-papo']:
            print('Modificando identificador das conversas do Facebook')

            def fModificar(row):
                return formatarIdentificadorFacebook(row['formatted_chat_name'])

            if self.config_custom["dono_celular"]['Facebook messenger'].strip() != '' and os.path.exists(
                    '.report\\contacts_db2'):
                self.df['formatted_chat_name'][self.df['app'] == 'Facebook messenger'] = self.df[
                    self.df['app'] == 'Facebook messenger'].apply(fModificar, axis=1)
            self.ultima_acao = 'modificar identificador do Facebook'

    def formatarDetalheAnexo(self):
        if self.config_custom['itens']['bate-papo']:
            def formataDetalhe(row):
                valor = str(row['attachment_details'])
                if valor != '' and 'https://' in valor:
                    return valor.split("https://")[0]
                return valor

            self.df['formatted_attachment_details'] = ''
            self.df['formatted_attachment_details'] = self.df.apply(formataDetalhe, axis=1)
            self.ultima_acao = 'formatar detalhe dos anexos'

    def classificarAnexos(self):
        # %%classifica os anexos em audio, imagem ou video
        if self.config_custom['itens']['bate-papo']:
            print('Analisando os anexos dos bate-papos')

            def analisaAnexo(row):
                if row['attachment_link']:
                    final = str(row['attachment_link'])[-7:]
                    if '.' in final:
                        ext = final.split('.')[-1]
                        if ext in self.config_custom["extensoes"]['imagem']:
                            return 'imagem'
                        elif ext in self.config_custom["extensoes"]['video']:
                            return 'video'
                        elif ext in self.config_custom["extensoes"]['audio']:
                            return 'audio'
                        else:
                            return 'arquivo'
                return ''

            self.df['attachment_type'] = self.df.apply(analisaAnexo, axis=1)
            self.ultima_acao = 'classificar anexos'


    def processar(self):
        # Ler o excel caso ainda não tenha sido feito isto
        if not self.dataframe_gerado:
            bate_papos = self.config_custom['itens']['bate-papo']
            smss = self.config_custom['itens']['sms']
            contatos = self.config_custom['itens']['contato']
            chamadas = self.config_custom['itens']['chamada']
            self.carregar()
            self.salvar()

        if self.config_custom['itens']['bate-papo']:
            self.excluirMensagensVazias()
            self.ordenarDataFrame()
            self.acrescentarColunasQuote()
            self.acrescentarColunas()
            self.formatarDetalheAnexo()
            self.classificarAnexos()
            self.classificarAnexosQuote()
            self.modificarIdentificadorWhatsapp()
            self.modificarIdentificadorFacebook()
            self.colorirMensagens()
        if self.config_custom['itens']['sms']:
            self.deletarColunasSmss()
            self.traduzirSmss()
        if self.config_custom['itens']['contato']:
            self.deletarColunasContatos()
        if self.config_custom['itens']['chamada']:
            self.deletarColunasChamadas()
        if self.config_custom['itens']['imagem']:
            self.deletarColunasImagens()
            self.acrescentarColunasImagens()
            self.removerImagensInvalidas()
        if self.config_custom['itens']['audio']:
            self.deletarColunasAudios()
            self.acrescentarColunasAudios()
            self.removerAudiosInvalidos()
        if self.config_custom['itens']['video']:
            self.deletarColunasVideos()
            self.acrescentarColunasVideos()
            self.removerVideosInvalidos()
        if self.config_custom['converter_formatos']:
            self.converterFormatos()
        self.processado = True

    def removerVideosInvalidos(self):
        print("Removendo vídeos sem extensão")
        self.df_videos['renderizar'] = self.df_videos['link'].apply(lambda x: True if pathlib.Path(x).suffix != "" else False)
        print("Removendo vídeos de tamanho zero")
        self.df_videos = self.df_videos[self.df_videos['size']>0]


    def removerAudiosInvalidos(self):
        print("Removendo audios sem extensão")
        self.df_audios['renderizar'] = self.df_audios['link'].apply(lambda x: True if pathlib.Path(x).suffix != "" else False)
        print("Removendo áudios de tamanho zero")
        self.df_audios = self.df_audios[self.df_audios['size']>0]

    def removerImagensInvalidas(self):
        print("Removendo imagens sem extensão")
        self.df_imagens['renderizar'] = self.df_imagens['link'].apply(lambda x: True if pathlib.Path(x).suffix != "" else False)
        print("Removendo imagens de tamanho zero")
        self.df_imagens = self.df_imagens[self.df_imagens['size']>0]

    def converterFormatos(self):            
        format_converter = FormatConverter()
        format_converter.overwrite = self.config_custom['converter_formatos_sobrescrever']
        format_converter.max_dim = self.config_custom['maxima_dimensao_video']
                    
        if self.config_custom['itens']['bate-papo']:
            df2 = self.df[self.df['attachment_type'].isin(['imagem', 'video'])]
            for i, row in df2.iterrows():
                filename = row['attachment_link']
                exists = self.consultFileConverted(filename)
                if not exists[0]:
                    res = format_converter.convert(filename)
                    if res['converted']:
                        self.df.at[i, 'midia_converted'] = True
                        self.df.at[i, 'attachment_link_before_conversion'] = filename
                        self.registryFileConverted(filename, res['filename'])
                        self.df.at[i, 'attachment_link'] = res['filename']
                else:
                    self.df.at[i, 'midia_converted'] = True
                    self.df.at[i, 'attachment_link_before_conversion'] = filename
                    self.df.at[i, 'attachment_link'] = exists[1]

        if self.config_custom['itens']['imagem']:
            for i, row in self.df_imagens.iterrows():
                filename = row['link']
                exists = self.consultFileConverted(filename)
                if not exists[0]:
                    res = format_converter.convert(filename)
                    if res['converted']:
                        self.df_imagens.at[i, 'midia_converted'] = True
                        self.df_imagens.at[i, 'link_before_conversion'] = filename
                        self.registryFileConverted(filename, res['filename'])
                        self.df_imagens.at[i, 'link'] = res['filename']
                else:
                    self.df_imagens.at[i, 'midia_converted'] = True
                    self.df_imagens.at[i, 'link_before_conversion'] = filename
                    self.df_imagens.at[i, 'link'] = exists[1]

        if self.config_custom['itens']['video']:
            for i, row in self.df_videos.iterrows():
                filename = row['link']
                exists = self.consultFileConverted(filename)
                if not exists[0]:
                    res = format_converter.convert(filename)
                    if res['converted']:
                        self.df_videos.at[i, 'midia_converted'] = True
                        self.df_videos.at[i, 'link_before_conversion'] = filename
                        self.registryFileConverted(filename, res['filename'])
                        self.df_videos.at[i, 'link'] = res['filename']
                else:
                    self.df_videos.at[i, 'midia_converted'] = True
                    self.df_videos.at[i, 'link_before_conversion'] = filename
                    self.df_videos.at[i, 'link'] = exists[1]


    def deleteConvertedMidias(self):
        if self.config_custom['itens']['bate-papo']:
            df2 = self.df[self.df['midia_converted']]
            for i, row in df2.iterrows():
                if os.path.exists(row['attachment_link_before_conversion']):
                    print(f"Deletando arquivo {row['attachment_link_before_conversion']}")
                    os.remove(row['attachment_link_before_conversion'])

        if self.config_custom['itens']['imagem']:
            df2 = self.df_imagens[self.df_imagens['midia_converted']]
            for i, row in df2.iterrows():
                if os.path.exists(row['link_before_conversion']):
                    print(f"Deletando arquivo {row['link_before_conversion']}")
                    os.remove(row['link_before_conversion'])

        if self.config_custom['itens']['video']:
            df2 = self.df_videos[self.df_vidoes['midia_converted']]
            for i, row in df2.iterrows():
                if os.path.exists(row['link_before_conversion']):
                    print(f"Deletando arquivo {row['link_before_conversion']}")
                    os.remove(row['link_before_conversion'])

    def listarTiposAnexos(self):
        df = self.df[self.df['attachment_link'] != ""]
        
        if self.config_custom['itens']['bate-papo']:
            extensoes = {}
            for i, row in df.iterrows():
                ext = pathlib.Path(row['attachment_link']).suffix.replace(".", "")
                if ext in extensoes.keys():
                    extensoes[ext] += 1
                else:
                    extensoes[ext] = 1
            print("\nANEXOS DE BATE-PAPO:")
            for ext in extensoes.keys():
                print(f"{ext}: {extensoes[ext]}")

        if self.config_custom['itens']['imagem']:
            extensoes = {}
            for i, row in df.iterrows():
                ext = pathlib.Path(row['link']).suffix.replace(".", "")
                if ext in extensoes.keys():
                    extensoes[ext] += 1
                else:
                    extensoes[ext] = 1
            print("\nIMAGENS GERAIS:")
            for ext in extensoes.keys():
                print(f"{ext}: {extensoes[ext]}")

        if self.config_custom['itens']['video']:
            extensoes = {}
            for i, row in df.iterrows():
                ext = pathlib.Path(row['link']).suffix.replace(".", "")
                if ext in extensoes.keys():
                    extensoes[ext] += 1
                else:
                    extensoes[ext] = 1
            print("\nVÍDEOS GERAIS:")
            for ext in extensoes.keys():
                print(f"{ext}: {extensoes[ext]}")

        if self.config_custom['itens']['audio']:
            extensoes = {}
            for i, row in df.iterrows():
                ext = pathlib.Path(row['link']).suffix.replace(".", "")
                if ext in extensoes.keys():
                    extensoes[ext] += 1
                else:
                    extensoes[ext] = 1
            print("\nÁUDIOS GERAIS:")
            for ext in extensoes.keys():
                print(f"{ext}: {extensoes[ext]}")
                 

    def classificarAnexosQuote(self):
        if self.config_custom['itens']['bate-papo']:
            def analisaAnexoQuote(row):
                if row['quote_attachment_link']:
                    final = str(row['quote_attachment_link'])[-7:]
                    if '.' in final:
                        ext = final.split('.')[-1]
                        if ext in self.config_custom["extensoes"]['imagem']:
                            return 'imagem'
                        elif ext in self.config_custom["extensoes"]['video']:
                            return 'video'
                        elif ext in self.config_custom["extensoes"]['audio']:
                            return 'audio'
                        else:
                            return 'arquivo'
                return ''

            self.df['quote_attachment_type'] = self.df.apply(analisaAnexoQuote, axis=1)
            self.ultima_acao = 'classificar anexos dos quotes'

    def colorirMensagens(self):
        if self.config_custom['itens']['bate-papo']:
            if self.config_custom['colorir_mensagens']:
                print('Atribuindo cores as mensagens de acordo com o remetente')

                def geraCor():
                    cores = ['#3e4444', '#405d27', '#034f84', '#c94c4c', '#618685', '#36486b', '#4040a1', '#bc5a45',
                             '#50394c', '#7a3b2e', ' #587e76']
                    i = 0
                    while True:
                        if i == 8:
                            i = 0
                        yield cores[i]
                        i += 1

                gerador = geraCor()
                self.df['color'] = ''
                gp = self.df.groupby('chat_name')
                participantes_atribuidos = {}
                for i, item in enumerate(gp.groups.keys()):

                    df2 = self.df[self.df['chat_name'] == item]
                    for i, row in df2.iterrows():
                        if not row['from'] in participantes_atribuidos:
                            participantes_atribuidos[row['from']] = next(gerador)
                        self.df['color'][self.df['id'] == row['id']] = participantes_atribuidos[row['from']]
                self.ultima_acao = 'colorir mensagens'

    
    def excluirMensagensVazias(self):
        print("Excluindo mensagens em vazias.")
        self.df = self.df[~((self.df['body'] == "") & (self.df['attachment'] == ""))]

    def marcarDestaques(self):
        if not self.processado:
            return
        if self.config_custom['itens']['bate-papo']:
            with codecs.open(".report\\destaques.txt", "r", "utf-8") as arq:
                destaques = arq.read()
            partes = destaques.split()
            itens = []
            for parte in partes:
                if '-' in parte:
                    de, ate = parte.split('-')
                    vals = [i for i in range(int(de), int(ate) + 1)]
                    itens += vals
                else:
                    itens.append(int(parte))
            self.df['tagged'][self.df['id'].isin(itens)] = True
            self.ultima_acao = 'marcar destaques'


    def renderizarPaginasVideos(self, chat_id, context):
        print(f"Renderizando paginas de videos do chat {chat_id}")
        # Gerar pagina de videos do chat
        df2 = self.df[(self.df['chat_id'] == chat_id) & (self.df['attachment_type'] == "video")]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_video'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page, per_page=self.config_custom['per_page_video'])
            context['pagination'] = pagination
            self.rend.render_template('videos.html', 'html_files\\videos{}_page_{}.html'.format(chat_id, page),
                                      context)

    def renderizarPaginasImagens(self, chat_id, context):
        print(f"Renderizando paginas de imagens do chat {chat_id}")
        # gerar página de imagens do chat
        df2 = self.df[(self.df['chat_id'] == chat_id) & (self.df['attachment_type'] == "imagem")]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_imagem'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page, per_page=self.config_custom['per_page_imagem'])
            context['pagination'] = pagination
            self.rend.render_template('imagens.html', 'html_files\\imagens{}_page_{}.html'.format(chat_id, page),
                                      context)

    def renderizarPaginasAudios(self, chat_id, context):
        print(f"Renderizando paginas de audios do chat {chat_id}")
        # gerar página de audios do chat
        df2 = self.df[(self.df['chat_id'] == chat_id) & (self.df['attachment_type'] == "audio")]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_audio'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_audio'])
            context['pagination'] = pagination
            self.rend.render_template('audios.html',
                                      'html_files\\audios{}_page_{}.html'.format(chat_id, page),
                                      context)

    def renderizarPaginaParticipantes(self, chat_id, chat_name, app):
        print(f"Renderizando pagina de participantes do chat {chat_id}")
        # gerar página de participantes
        df2 = self.df[self.df['chat_id'] == chat_id]
        participantes = getParticipantes(df2, self.config_custom['tipo_telefone'])
        self.rend.render_template('participantes.html', 'html_files\\participantes{}.html'.format(chat_id),
                                  {'participantes': participantes, 'chat_name': chat_name, 'app': app})

    def renderizarPaginasTodosAudios(self, app=None):
        print(f"Renderizando paginas de todos os audios do aplicativo {app}")
        df2 = self.df[self.df['attachment_type'] == "audio"]
        app_string = ""
        if app is not None:
            app_string = app
            df2 = df2[df2['app'] == app]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_audio'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_audio'])
            self.rend.render_template('todos-audios.html', 'html_files/todos-audios{}_page_{}.html'.format(app, page),
                                      {'pagination': pagination, 'app': app_string})

    def renderizarPaginasTodosVideos(self, app=None):
        print(f"Renderizando paginas de todos os vídeos do aplicativo {app}")
        df2 = self.df[self.df['attachment_type'] == "video"]
        app_string = ""
        if app is not None:
            app_string = app
            df2 = df2[df2['app'] == app]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_video'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_video'])

            self.rend.render_template('todos-videos.html',
                                      'html_files/todos-videos{}_page_{}.html'.format(app_string, page),
                                      {'pagination': pagination, 'app': app_string})

    def renderizarPaginasTodasImagens(self, app=None):
        print(f"Renderizando paginas de todas as imagens do aplicativo {app}")
        df2 = self.df[self.df['attachment_type'] == "imagem"]
        app_string = ""
        if app is not None:
            app_string = app
            df2 = df2[df2['app'] == app]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_imagem'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_imagem'])
            app_string = app if app is not None else ""
            self.rend.render_template('todas-imagens.html',
                                      'html_files/todas-imagens{}_page_{}.html'.format(app_string, page),
                                      {'pagination': pagination, 'app': app_string})

    def renderizarPaginasImagensGerais(self):
        print("Renderizando paginas das imagens gerais")
        df2 = self.df_imagens[self.df_imagens['renderizar']]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_imagem'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_imagem'])
            self.rend.render_template('imagens-gerais.html', 'html_files/imagens-gerais_page_{}.html'.format(page),
                                      {'pagination': pagination})

    def renderizarPaginasAudiosGerais(self):
        print("Renderizando paginas das audios gerais")
        df2 = self.df_audios[self.df_audios['renderizar']]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_audio'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_audio'])
            self.rend.render_template('audios-gerais.html', 'html_files/audios-gerais_page_{}.html'.format(page),
                                      {'pagination': pagination})

    def renderizarPaginasVideosGerais(self):
        print("Renderizando paginas dos vídeos gerais")
        df2 = self.df_videos[self.df_videos['renderizar']]
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_video'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_imagem'])
            self.rend.render_template('videos-gerais.html', 'html_files/videos-gerais_page_{}.html'.format(page),
                                      {'pagination': pagination})

    def renderizarPaginasLinhaTempo(self):
        print("Renderizando paginas da linha do tempo")
        df2 = self.df.sort_values(by=['timestamp'], ascending=[True])
        n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_linha_tempo'])
        for i in range(n_pages):
            page = i + 1
            pagination = getPage(df2, total_pages=n_pages, page=page,
                                 per_page=self.config_custom['per_page_linha_tempo'])
            self.rend.render_template('linha-tempo.html', 'html_files/linha-tempo_page_{}.html'.format(page),
                                      {'pagination': pagination})

    def marcarPaginaChat(self, df_filtrado, page):
        """Marca no data frame em qual página foi renderizada um determinado conjunto de mensagens de um chat"""
        for i, row in df_filtrado.iterrows():
            self.df.at[i, 'page'] = page

    def renderizar(self, mostrar_num_mensagem=False, destaques=False):
        if not self.processado:
            self.processar()
            self.salvar()
        apps = []
        if self.config_custom['itens']['bate-papo']:
            print('Renderizando bate-papos')
            copiaArquivosNecessarios()

            gp_app = self.df.groupby('app')
            self.chats_gerados = []
            apps = gp_app.groups.keys()
            for app in apps:
                df_app = self.df[self.df.app == app]
                gp = df_app.groupby('chat_id')
                chats_app_gerados = []  # chats comente relacionados a este app
                for item in gp.groups.keys():
                    print(f"Renderizando chat '{item}' do aplicativo {app}")
                    df2 = self.df[self.df['chat_id'] == item]
                    chat_gerando = {'link': 'chat{}_page_1.html'.format(item),
                                    'nome': df2.iloc[0]['formatted_chat_name'],
                                    'origem': app, 'n_men': len(df2),
                                    'avatar_chat': df2.iloc[0]['avatar_chat'],
                                    'data_criacao': df2.iloc[0]['start_time'],
                                    'ultimo_acesso': df2.iloc[0]['last_activity']}
                    n_pages = getPage(df2, only_count=True, per_page=self.config_custom['per_page_chat'])
                    for i in range(n_pages):
                        page = i + 1
                        pagination = getPage(df2, total_pages=n_pages, page=page, per_page=self.config_custom['per_page_chat'])
                        context = {"pagination": pagination, "numero_chat": item,
                                   "identificador_formatado": df2.iloc[0]['formatted_chat_name'],
                                   "origem": df2.iloc[0]['app'],
                                   "mostrar_num_mensagem": mostrar_num_mensagem, 'n_imagens': countImages(df2),
                                   'n_videos': countVideos(df2), 'n_audios': countAudios(df2)}
                        self.rend.render_template('chat.html', 'html_files\\chat{}_page_{}.html'.format(item, page),
                                                  context)

                        self.marcarPaginaChat(pagination['df'], page)

                    self.renderizarPaginasVideos(item, context)
                    self.renderizarPaginasImagens(item, context)
                    self.renderizarPaginasAudios(item, context)
                    self.renderizarPaginaParticipantes(item, df2.iloc[0]['formatted_chat_name'], app)

                    self.chats_gerados.append(chat_gerando)
                    chats_app_gerados.append(chat_gerando)

                self.renderizarPaginasTodosAudios(app=app)
                self.renderizarPaginasTodosVideos(app=app)
                self.renderizarPaginasTodasImagens(app=app)
                chats_app_gerados = sorted(chats_app_gerados, key=lambda x: x['n_men'], reverse=True)
                self.rend.render_template('chats.html', "html_files\\chats_{}.html".format(app),
                                          {'chats': chats_app_gerados, 'app': app, 'total_audios': countAudios(df_app),
                                           'total_imagens': countImages(df_app), 'total_videos': countVideos(df_app)})

            self.renderizarPaginasLinhaTempo()
            # self.chats_gerados = sorted(self.chats_gerados, key=lambda x: x['origem'], reverse=True)

        self.n_renderizacoes += 1
        if self.config_custom['itens']['chamada']:
            self.renderizarChamadas()
        if self.config_custom['itens']['sms']:
            self.renderizarSmss()
        if self.config_custom['itens']['contato']:
            self.renderizarContatos()
        if self.config_custom['itens']['imagem']:
            self.renderizarPaginasImagensGerais()
        if self.config_custom['itens']['audio']:
            self.renderizarPaginasAudiosGerais()
        if self.config_custom['itens']['video']:
            self.renderizarPaginasVideosGerais()
        nome_arquivo = "Relatório simplificado.html"

        self.rend.render_template('main.html', nome_arquivo, {'destaques': destaques, 'apps': apps,
                                                              'rg': self.config_custom['info']['RG'],
                                                              'sinf': self.config_custom['info']['SINF'],
                                                              'objeto': self.config_custom['info']['objeto'],
                                                              'bate_papos': self.config_custom['itens']['bate-papo'],
                                                              'smss': self.config_custom['itens']['sms'],
                                                              'chamadas': self.config_custom['itens']['chamada'],
                                                              'contatos': self.config_custom['itens']['contato'],
                                                              'imagens': self.config_custom['itens']['imagem'],
                                                              'videos': self.config_custom['itens']['video'],
                                                              'audios': self.config_custom['itens']['audio']})
        self.rend.render_template('home.html', "html_files\\home.html",
                                  {'destaques': destaques, 'config_custom': self.config_custom})
        self.salvar()
        self.ultima_acao = 'renderizar'
        print("Arquivos renderizados")

    def renderizarDestaques(self, mostrar_num_mensagem=False):
        if self.n_renderizacoes == 0:
            self.renderizar()
        nome_arquivo = "Relatório simplificado.html"
        gp_app = self.df.groupby('app') if  self.config_custom['itens']['bate-papo'] else None
        apps = gp_app.groups.keys() if gp_app else None

        self.rend.render_template('main.html', nome_arquivo, {'destaques': True, 'apps': apps,
                                                              'rg': self.config_custom['info']['RG'],
                                                              'sinf': self.config_custom['info']['SINF'],
                                                              'objeto': self.config_custom['info']['objeto'],
                                                              'bate_papos': self.config_custom['itens']['bate-papo'],
                                                              'imagens': self.config_custom['itens']['imagem'],
                                                              "videos": self.config_custom['itens']['video'],
                                                              "chamadas": self.config_custom['itens']['chamada'],
                                                              "contatos": self.config_custom['itens']['contato'],
                                                              "smss": self.config_custom['itens']['sms'],
                                                              "audios": self.config_custom['itens']['audio']})
        self.rend.render_template('home.html', "html_files\\home.html",
                                  {'destaques': True, 'config_custom': self.config_custom})
        context = {"mostrar_num_mensagem": mostrar_num_mensagem}
        if self.config_custom['itens']['bate-papo']:
            context['mensagens_df'] = self.df[self.df['tagged']].sort_values(by=['timestamp'], ascending=[True])
        if self.config_custom['itens']['imagem']:
            context['imagens_df'] = self.df_imagens[self.df_imagens['tagged']]
        if self.config_custom['itens']['audio']:
            context['audios_df'] = self.df_audios[self.df_audios['tagged']]
        if self.config_custom['itens']['video']:
            context['videos_df'] = self.df_videos[self.df_videos['tagged']]
        self.rend.render_template('destaques.html', 'html_files/destaques.html', context)
        self.ultima_acao = 'renderizar destaques'
        print('Destaques renderizados')

    def renderizarDestaquesParaWord(self, qtdporfigura=5, mostrar_num_mensagem=False):
        if not self.processado:
            self.processar()
            self.salvar()
        pasta = "html_files"
        mensagens = self.df[self.df['tagged_word'] & (
                (self.df['attachment_link'] == '') | ((self.df['attachment_type'] == 'imagem')))].sort_values(
            by=['timestamp'], ascending=[True])
        n_parts = int(mensagens.shape[0] / qtdporfigura)
        print("n_parts: " + str(n_parts))
        rest = mensagens.shape[0] % qtdporfigura
        print("rest: " + str(rest))
        arquivos_gerados = []
        for i in range(n_parts):
            primeiro = i * qtdporfigura
            context = {"mensagens": mensagens.iloc[primeiro:primeiro + qtdporfigura],
                       "mostrar_num_mensagem": mostrar_num_mensagem}
            arquivo = f"html_files\\destaques_word_{i+1}.html"
            self.rend.render_template("destaques_word.html", arquivo, context)
            arquivos_gerados.append(os.path.join(os.getcwd(), arquivo))
        if rest > 0:
            primeiro = n_parts * qtdporfigura
            context = {"mensagens": mensagens.iloc[primeiro:primeiro + rest],
                       "mostrar_num_mensagem": mostrar_num_mensagem}
            arquivo = f"html_files\\destaques_word_{n_parts + rest}.html"
            self.rend.render_template("destaques_word.html", arquivo, context)
            arquivos_gerados.append(os.path.join(os.getcwd(), arquivo))
        return arquivos_gerados

    def getDestaquesWordImagens(self):
        df = self.df_imagens[self.df_imagens['tagged_word']]
        lista = []
        for i, row in df.iterrows():
            lista.append(os.path.join(os.getcwd(), row['link']))
        return lista

    def renderizarSmss(self):
        if self.config_custom['itens']['sms']:
            copiaArquivosNecessarios()
            self.rend.render_template('smss.html', 'html_files\\sms.html', {'df': self.df_smss})
            self.ultima_acao = 'Renderização de SMSs'

    def renderizarContatos(self):
        if self.config_custom['itens']['contato']:
            copiaArquivosNecessarios()
            self.rend.render_template('contatos.html', 'html_files\\contatos.html', {'df': self.df_contatos})
            self.ultima_acao = 'Renderização de contatos'

    def renderizarChamadas(self):
        if self.config_custom['itens']['chamada']:
            copiaArquivosNecessarios()
            self.rend.render_template('chamadas.html', 'html_files\\chamadas.html', {'df': self.df_chamadas})
            self.ultima_acao = 'Renderização de chamadas'

    def copiarAvatarsAndroid(self):
        if os.path.exists('.report\Avatars'):
            if os.path.exists('html_files\\Avatars'):
                shutil.rmtree('html_files\\Avatars')
            copyanything('.report\\Avatars', 'html_files\\Avatars')
        else:
            print(
                "A pasta '.report\Avatars' não existe. É necessário antes copiar a pasta com os avatares para dentro de '.report' mantendo ela nomeada como 'Avatars'")

    def renomearAvatarsAndroid(self):
        pasta = "html_files\\Avatars"
        if os.path.exists(pasta):
            for arq in os.listdir(pasta):
                res = re.search(r'(.*((s.whatsapp\.net)|(g\.us)))\..*', arq)
                if res:
                    try:
                        os.rename("{}\\{}".format(pasta, arq), "{}\\{}".format(pasta, res.groups()[0] + '.jpg'))
                    except:
                        print("Erro no arquivo: ", arq)
            try:
                os.rename("{}\\me.j".format(pasta), "{}\\me.jpg".format(pasta))
            except:
                print("O arquivo 'me.j', que é o avatar do proprietário do celular, não foi encontrado")
            self.ultima_acao = 'renomear avatars'

    def copiarAvatarsIphone(self):
        if os.path.exists('.report\\Profile'):
            if os.path.exists('html_files\\Avatars'):
                shutil.rmtree('html_files\\Avatars')
            os.mkdir('html_files\\Avatars')
            avatars = get_last_avatar_names('.report\\Profile')
            for avatar in avatars:
                shutil.copy(f".report\\Profile\\{avatar[0]}", f"html_files\\Avatars\\{avatar[2]}.jpg")
            # copyanything('.report\\Profile', 'html_files\\Avatars')
        else:
            print(
                "A pasta '.report\Profile' não existe. É necessário antes copiar a pasta com os avatares para dentro de '.report' mantendo ela nomeada como 'Profile'")

    # def renomearAvatarsIphone(self):
    #     pasta = "html_files\\Avatars"
    #     if os.path.exists(pasta):
    #         for arq in os.listdir(pasta):
    #             try:
    #                 os.rename("{}\\{}".format(pasta, arq),
    #                             "{}\\{}".format(pasta, res.groups()[1] + '@s.whatsapp.net.jpg'))
    #             except:
    #                 print("Erro no arquivo: ", arq)
    #         try:
    #             os.rename("{}\\Photo.jpg".format(pasta), "{}\\me.jpg".format(pasta))
    #         except:
    #             print("O arquivo 'Photo.jpg', que é o avatar do proprietário do celular, não foi encontrado")
    #         self.ultima_acao = 'renomear avatars Iphone'


    def addExtracaoAeb(self, html_file, nome_link):
        pasta_trabalho = os.path.dirname(html_file)
        pasta_html_files = pasta_trabalho + "\\html_files"
        if os.path.exists( "html_files\\html_files"):
            shutil.rmtree("html_files\\html_files")
        if os.path.exists("html_files\\files"):
            shutil.rmtree("html_files\\files")
        if os.path.exists("html_files\\chats-aeb.html"):
            os.remove("html_files\\chats-aeb.html")
        copyanything(pasta_html_files, "html_files\\html_files")
        copyanything(pasta_trabalho + "\\files", "html_files\\files")
        shutil.copyfile(html_file, "html_files\\chats-aeb.html")
        gp_app = self.df.groupby('app')
        apps = gp_app.groups.keys()
        self.rend.render_template('main.html', "Relatório simplificado.html", {'destaques': True, 'apps': apps,
                                                              'rg': self.config_custom['info']['RG'],
                                                              'sinf': self.config_custom['info']['SINF'],
                                                              'objeto': self.config_custom['info']['objeto'],
                                                              'bate_papos': self.config_custom['itens']['bate-papo'],
                                                              'imagens': self.config_custom['itens']['imagem'],
                                                              "videos": self.config_custom['itens']['video'],
                                                              "chamadas": self.config_custom['itens']['chamada'],
                                                              "contatos": self.config_custom['itens']['contato'],
                                                              "smss": self.config_custom['itens']['sms'], 'link_adicional': {"caption": nome_link, "nome_arquivo": "chats-aeb.html"}})


if __name__ == "__main__":
    os.chdir(r'C:\Users\renato\Desktop\temp\Relatório Iphone\Apple_iPhone 7 Plus (A1784)')
    hd = Handler()
    hd.carregarSalvo()
    hd.converterFormatos()