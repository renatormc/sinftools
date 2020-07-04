# -*- coding: utf-8 -*-
"""Script serve para ser utilizado dentro do Physical Analiser"""
import json
import codecs
import glob
import os
import time
import datetime
import re


class Ufed():
    #copia arquivo do sistema do UFED para fora do UFED
    def CopiarArquivo(self, arqOri, dirDestStr, arqDestStr):
        if not os.path.exists(dirDestStr):
            os.mkdir(dirDestStr)
        try:
            with open(dirDestStr + "\\" + arqDestStr,"wb") as arqDest:
                arqOri.seek(0)
                arqDest.write(arqOri.read())
        except:
            pass
        
    def safestr(self, obj):
        if isinstance(obj, str):
            return obj
        else:
            return str(obj)

    def localiza_arquivo(self, arquivo):
        for fs in ds.FileSystems:
            for f in fs.Search(arquivo):
                if f.Type == Data.Files.NodeType.File:
                    print(f.AbsolutePath)

    def localiza_diretorio(self, diretorio):
        for fs in ds.FileSystems:
            for f in fs.Search(diretorio):
                if f.Type == Data.Files.NodeType.Directory:
                    print(f.AbsolutePath)

    def msgstore(self):
        resposta = []
        for fs in ds.FileSystems:
            for f in fs.Search('msgstore.db'):
                if (f.Type == Data.Files.NodeType.File) and (f.Name.endswith('msgstore.db')):
                   return resposta
        return resposta

    def wa(self):
        for fs in ds.FileSystems:
            for f in fs.Search('wa.db'):
                if f.Type == Data.Files.NodeType.File:
                    return f

    def logs(self):
        for fs in ds.FileSystems:
            for f in fs.Search('logs.db'):
                if f.Type == Data.Files.NodeType.File:
                    return f

    def mmssms(self):
        for fs in ds.FileSystems:
            for f in fs.Search('mmssms.db'):
                if f.Type == Data.Files.NodeType.File:
                    return f

    def preferences(self):
        for fs in ds.FileSystems:
            for f in fs.Search('com.whatsapp_preferences.xml'):
                if f.Type == Data.Files.NodeType.File:
                    return f
                    
    def LocalizaPastaAvatar(self):
        for fs in ds.FileSystems:
            for f in fs.Search('com.whatsapp/files/Avatars'):
                if f.Type == Data.Files.NodeType.Directory:
                    return f

    def LocalizaPastaAvatarIphone(self):
        for fs in ds.FileSystems:
            for f in fs.Search('/Profile'):
                if f.Type == Data.Files.NodeType.Directory:
                    return f

    def LocalizaPastaAnexos(self):
        for fs in ds.FileSystems:
            for f in fs.Search('WhatsApp/Media'):
                if f.Type == Data.Files.NodeType.Directory:
                    return f
    
    def exportar_avatars(self, pasta):
        try:
            dir = self.LocalizaPastaAvatar()
            for arq in ds.FileSystems[dir.FileSystem.Name][dir.AbsolutePath]:
                self.CopiarArquivo(arq, pasta + "\\Avatars", arq.Name)
        except:
            print("Não foi possível localizar e extrair a pasta Avatars do Whatsapp, faça isso manualmente")

    def exportar_avatars_iphone(self, pasta):
        try:
            dir = self.LocalizaPastaAvatarIphone()
            for arq in ds.FileSystems[dir.FileSystem.Name][dir.AbsolutePath]:
                self.CopiarArquivo(arq, pasta + "\\Profile", arq.Name)
        except:
            print("Não foi possível localizar e extrair a pasta Profile, faça isso manualmente")
        

    def exportar_anexos(self):
        try:
            dir = self.LocalizaPastaAnexos()
            for node in dir.GetAllNodes():
                if node.Type == NodeType.File:
                    self.CopiarArquivo(node, "C:\\ScriptsUFED\\Dados\\Anexos_WhatsApp", node.Name)
        except:
            print("Não foi possível localizar e extrair a pasta contendo os anexos do Whatsapp, faça isso manualmente")
            if not os.path.exists('C:/ScriptsUFED/Dados/Anexos_WhatsApp'):
                    os.mkdir('C:/ScriptsUFED/Dados/Anexos_WhatsApp')
    def exportar_msgstore(self):
        for arquivo in self.msgstore():
            print('Extraindo ',arquivo)
            self.CopiarArquivo(arquivo, r'C:\ScriptsUFED\Add\Extrair do sqlite\dados',arquivo.Name)
        

ufed = Ufed()
