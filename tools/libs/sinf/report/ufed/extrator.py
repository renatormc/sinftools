import json
import codecs

class Extrator:
    def setNomeArquivo(self, arquivo):
        self.nome_arquivo = arquivo
    
    def setFuncaoRegistro(self, funcao):
        self.funcao = funcao

    def extrair(self, colecao):
        registros = [self.funcao(item) for item in colecao]
        with codecs.open(self.nome_arquivo,"w",'utf-8') as outfile:
	        outfile.write(json.dumps(registros, ensure_ascii=False, indent=2))

