import os
import shutil
import hashlib
from sinf.sync.statistic import Statistic


def calculateHash(file):
    m = hashlib.sha256()
    m.update(open(file,'rb').read())
    return m.digest()


def compareFiles(file1, file2, ctime=True, size=True, hash=False):
    if ctime and os.path.getmtime(file1) != os.path.getmtime(file2):
        return False
    if size and os.path.getsize(file1) != os.path.getsize(file2):
        return False
    if hash and calculateHash(file1) != calculateHash(file2):
        return False
    return True


class Updater:
    def __init__(self, from_, to):
        self.from_ = from_ 
        self.to = to
        self.folders_delete = []
        self.folders_create = []
        self.folders_from = []
        self.folders_to = []
        self.files_delete = []
        self.files_create = []
        self.files_replace = []
    

    def analizeFolders(self):
        #Analisar from
        for root, dirs, files in os.walk(self.from_):
            for dir_ in dirs:
                self.folders_from.append((os.path.join(root, dir_).replace(self.from_ + "\\", "")))

        #analisar to
        for root, dirs, files in os.walk(self.to):
            for dir_ in dirs:
                self.folders_to.append((os.path.join(root, dir_).replace(self.to + "\\", "")))

        for folder in self.folders_from:
            if not folder in self.folders_to:
                self.folders_create.append(folder)

        for folder in self.folders_to:
            if not folder in self.folders_from:
                self.folders_delete.append(folder)

    def analizeFiles(self, hash=False):
        for root, dirs, files in os.walk(self.from_):
            for file in files:
                file_ = os.path.join(root, file).replace(self.from_ + "\\", "")
                if not os.path.exists(os.path.join(self.to, file_)):
                    self.files_create.append(file_)
                elif not compareFiles(os.path.join(self.to, file_), os.path.join(self.from_, file_), hash=hash):
                    self.files_replace.append(file_)
        for root, dirs, files in os.walk(self.to):
            for file in files:
                file_ = os.path.join(root, file).replace(self.to + "\\", "")
                if not os.path.exists(os.path.join(self.from_, file_)):
                    self.files_delete.append(file_)
    
    def syncFolders(self, exec_=True):
        for folder in self.folders_delete:
            path = os.path.join(self.to, folder)
            if os.path.exists(path):
                ok = ""
                if exec_:
                    shutil.rmtree(path)
                    ok = " - OK "
                print("Deletar pasta {}{}".format(folder, ok))
        
        for folder in self.folders_create:
            path = os.path.join(self.to, folder)
            if not os.path.exists(path):
                ok = ""
                if exec_:
                    os.makedirs(path)
                    ok = " - OK"
                print("Copiar pasta {}{}".format(folder, ok))

    def syncFiles(self, exec_=True):
        for file in self.files_delete:
            ok = ""
            if exec_:
                os.remove(os.path.join(self.to, file))
                ok = " - OK"
            print("Deletar arquivo {}{}".format(file, ok))

        for file in self.files_create:
            ok = ""
            if exec_:
                shutil.copy2(os.path.join(self.from_, file), os.path.join(self.to, file))
                ok = " - OK"
            print("Copiar arquivo {}{}".format(file, ok))

        for file in self.files_replace:
            ok = ""
            if exec_:
                shutil.copy2(os.path.join(self.from_, file), os.path.join(self.to, file))
                ok = " - OK"
            print("Substituir arquivo {}{}".format(file, ok))

    def analizeAndSync(self, exec_=True, hash=False):
        self.analizeFolders()
        self.syncFolders(exec_=exec_)
        self.analizeFiles(hash=hash)
        self.syncFiles(exec_=exec_)

    def getStatistics(self):
        size_copy = 0
        for file in self.files_create:
            size_copy += os.path.getsize(os.path.join(self.from_, file))
        size_replace = 0
        for file in self.files_replace:
            size_replace += os.path.getsize(os.path.join(self.from_, file))
        size_delete = 0
        for file in self.files_delete:
            size_delete += os.path.getsize(os.path.join(self.to, file))
        retorno = Statistic()
        retorno.n_folders_create = len(self.folders_create)
        retorno.n_folders_delete = len(self.folders_delete)
        retorno.files_create = {"n": len(self.files_create), "size": size_copy}
        retorno.files_replace = {"n": len(self.files_replace), "size": size_replace}
        retorno.files_delete = {"n": len(self.files_delete), "size": size_delete}
        return retorno
