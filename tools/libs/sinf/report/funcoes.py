import os
import shutil
# from sinf.report.config import config
import pandas as pd
import urllib
from sinf.report.auxiliar import copyanything
import codecs
import json

sinftools_dir = os.getenv("SINFTOOLS")
script_dir = os.path.dirname(os.path.realpath(__file__))


def get_file_config():
    base_dir = ""
    for i in range(5):
        base_dir += "..\\"
        file_ = f"{base_dir}case_info.json"
        if os.path.exists(file_):
            return file_

def iniciar(dir, versao_ufed):
    """Cria a pasta .report e a pasta html"""
    os.chdir(dir)
    if os.path.exists(".report"):
        resposta = input("Já existe um projeto nesta pasta. Deseja deletá-lo e começar do zero um novo? (s/n): ")
        if resposta not in ['s', 'S']:
            return None
        shutil.rmtree(".report")
        if os.path.exists("html_files"):
            shutil.rmtree("html_files")

    if not os.path.exists('.report\\config.json'):
        arquivo = "{}\\versions_pa\\config_files\\{}.json".format(script_dir, versao_ufed)
        if os.path.exists(arquivo):
            if not os.path.exists('.report'):
                os.mkdir('.report')
            shutil.copy2(arquivo, '.report\config.json')
            
            #Acrescentar nome do caso
            file_ = get_file_config()
            if file_ is not None:
                with codecs.open(".report\config.json", "r", "utf-8") as f:
                    data = json.load(f)
                with codecs.open(file_, "r", "utf-8") as f:
                    info = json.load(f)
                data['info']['RG'] = info['RG']
                data['info']['SINF'] = info['SINF']
                with codecs.open(".report\\config.json", "w", "utf-8") as f:
                    f.write(json.dumps(data, ensure_ascii=False, indent=2))

            open('.report\\destaques.txt', 'a').close()
        else:
            versoes = [s.replace('.json', '') for s in os.listdir("{}\\versions_pa\\config_files".format(script_dir))]
            print("Não há suporte para esta versão ainda.")
            print("Versões disponíveis: \n{}".format('\n'.join(versoes)))
            return None
    copyanything("{}\\notebooks".format(script_dir), ".report\\notebooks")
    copiaArquivosNecessarios()
    # hd = handler.Handler()
    # hd.copiaArquivosNecessarios()
    # return hd


def copiaArquivosNecessarios():
    if not os.path.exists('html_files'):
        copyanything("{}\\html_files".format(script_dir), "html_files")
    os.system("attrib +h " + "html_files")

def listaDestaques(df):
    return " ".join(df['id'].apply(str))


def getVersoesDisponiveis():
    return [s.replace('.json', '') for s in os.listdir("{}\\versions_pa\\config_files".format(script_dir))]


class RemovedorArquivos:
    def __init__(self):
        self.df = pd.read_pickle('.report\\save\\df_chats')
        self.df = self.df[self.df['attachment_link'] != '']

    def setPastaAnexos(self, pasta):
        self.pasta_anexos = pasta

    def temReferencia(self, valor):
        texto = urllib.parse.quote(valor.replace('\\', '/'))
        df2 = self.df[self.df['attachment_link'].str.contains(texto)]
        if len(df2) > 0:
            return True
        return False

    def deletarArquivosSemReferencia(self):
        for root, dirs, files in os.walk(os.path.join(os.getcwd(), self.pasta_anexos)):
            for file in files:
                arquivo = os.path.relpath(os.path.join(root, file), os.getcwd())
                if not self.temReferencia(arquivo):
                    os.remove(arquivo)
                    print("Removendo arquivo {}".format(arquivo))
            for dir_ in dirs:
                diretorio = os.path.relpath(os.path.join(root, dir_), os.getcwd())
                if len(os.listdir(diretorio)) == 0:
                    os.rmdir(diretorio)
                    print("Removendo diretório vazio {}".format(dir_))


def op_destaques_word(legenda, qtd_por_figura, handler):
    import win32com.client as win32
    import imgkit
    legenda = str(legenda).strip()
    quantidade_por_figura = int(qtd_por_figura)

    arquivos = handler.renderizarDestaquesParaWord(qtdporfigura=quantidade_por_figura)

    word = word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.ActiveDocument
    path_wkthmltoimage = f'{sinftools_dir}\\extras\\wkhtmltox\\bin\\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
    lista = []
    for i, arquivo in enumerate(arquivos):
        arq_nome = f".report\\destaques_{i+1}.jpg"
        try:
            imgkit.from_file(arquivo, arq_nome, config=config)
        except:
            pass
        lista.append(os.path.join(os.getcwd(), arq_nome))
    n_col = 1
    n_row = len(lista)
    if n_row > 0:
        tabela = doc.Tables.Add(word.Selection.Range, n_row, n_col)
        tabela.Borders.InsideLineStyle = 0
        tabela.Borders.OutsideLineStyle = 0
        for i in range(1, n_row + 1):
            for j in range(1, n_col + 1):
                k = n_col * (i - 1) + j - 1
                if k >= len(lista):
                    break
                arq_nome = f"{lista[k]}"
                shape = tabela.Cell(i, j).Range.InlineShapes.AddPicture(arq_nome)
                shape.Select
                tabela.Cell(i, j).Range.Paragraphs(1).Alignment = win32.constants.wdAlignParagraphCenter
                caption = shape.Range.InsertCaption(Label="Figura", Title=f" - {legenda}",
                                                    Position=win32.constants.wdCaptionPositionBelow)
        tabela.Select()
        word.Selection.Style = doc.Styles("Legenda")

def op_destaques_word_imagens(n_col, lista):
    import win32com.client as win32
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.ActiveDocument
    if len(lista) % n_col != 0:
        n_row = int(len(lista) / n_col) + 1
    else:
        n_row = int(len(lista) / n_col)
    tabela = doc.Tables.Add(word.Selection.Range, n_row, n_col)
    tabela.Borders.InsideLineStyle = 1
    tabela.Borders.OutsideLineStyle = 1
    for i in range(1, n_row + 1):
        for j in range(1, n_col + 1):
            k = n_col * (i - 1) + j - 1
            if k >= len(lista):
                break
            tabela.Cell(i, j).Range.InlineShapes.AddPicture(lista[k])


def get_columns_excel(versao):
    with codecs.open(f"{script_dir}\\versions_pa\\excel_columns\\{versao}.json", "r", "utf-8") as f:
        data = json.load(f)
    return data


def findXLSX():
    excel_encontrados = []
    for node in os.listdir():
        if node.endswith('.xlsx'):
            excel_encontrados.append(node)
    qtd = len(excel_encontrados)
    if qtd == 1:
        return excel_encontrados[0]
    if qtd == 0:
        print(
            "Não foi encontrado nenhum arquivo do tipo \"xlsx\" na pasta de trabalho. Para funcionar o sistema precisa utilizar o relatório gerado pelo PA no formato \"xlsx\".")
        return None
    if qtd > 1:
        print("Foram encontrados mais de um arquivo do tipo \"xlsx\". Qual deles é o relatório gerado pelo PA?")
        for i, arq in enumerate(excel_encontrados):
            print(f"{i+1}- {arq}")
        while True:
            try:
                op = input("op: ")
                op = int(op) - 1
                return excel_encontrados[op]
            except:
                print("Opção inválida.")

def get_config():
    with codecs.open(".report\\config.json", "r", "utf-8") as f:
        data = json.load(f)
    return data

def countImages(df):
    return df[df['attachment_type'] == "imagem"].shape[0]

def countVideos(df):
    return df[df['attachment_type'] == "video"].shape[0]

def countAudios(df):
    return df[df['attachment_type'] == "audio"].shape[0]

if __name__ == "__main__":
    get_file_config()
