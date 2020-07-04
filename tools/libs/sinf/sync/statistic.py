class Statistic:
    def __init__(self):
        self.n_folders_create = 0
        self.n_folders_delete = 0
        self.files_create = {"n": 0 , "size": 0}
        self.files_replace = {"n": 0 , "size": 0}
        self.files_delete = {"n": 0 , "size": 0}

    def __add__(self, other):
        retorno = Statistic()
        retorno.n_folders_create = self.n_folders_create + other.n_folders_create
        retorno.n_folders_delete = self.n_folders_delete + other.n_folders_delete
        retorno.files_create["n"] = self.files_create["n"] + other.files_create["n"]
        retorno.files_replace["n"] = self.files_replace["n"] + other.files_replace["n"]
        retorno.files_delete["n"] = self.files_delete["n"] + other.files_delete["n"]
        retorno.files_create["size"] = self.files_create["size"] + other.files_create["size"]
        retorno.files_replace["size"] = self.files_replace["size"] + other.files_replace["size"]
        retorno.files_delete["size"] = self.files_delete["size"] + other.files_delete["size"]
        return retorno

    def print(self):
        print("\n\nRESULTADO DA ANALISE")
        print("{} pastas serão adicionadas".format(self.n_folders_create))
        print("{} pastas serão deletadas".format(self.n_folders_delete))
        print("{} arquivos serão adicionados, totalizando {} bytes".format(self.files_create['n'],
                                                                           self.files_create['size']))
        print("{} arquivos serão substituidos, totalizando {} bytes".format(self.files_replace['n'],
                                                                            self.files_replace['size']))
        print("{} arquivos serão deletados, totalizando {} bytes".format(self.files_delete['n'],
                                                                         self.files_delete['size']))
