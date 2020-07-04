import sys
import os
import io
import codecs
import hashlib
from tqdm import tqdm


# def progress(count, total, suffix=''):
#     bar_len = 60
#     filled_len = int(round(bar_len * count / float(total)))

#     percents = round(100.0 * count / float(total), 1)
#     bar = '=' * filled_len + '-' * (bar_len - filled_len)

#     sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
#     sys.stdout.flush()  # As suggested by Rom Ruben

NomeDoArquivoHash = 'Hash.txt'
NomeDoArquivoHashdoHash = 'Hash do hash.txt'

class Hasher:
    def __init__(self):
        self.directory = "."
        self.directory_hash_hash = ".."

    def listarArquivos(self, rootDir):
        arquivos = []
        list_dirs = os.walk(rootDir)
        for root, dirs, files in list_dirs:
            for f in files:
                arquivos.append(os.path.join(root, f))
        return arquivos

    def sha512(self, fname):
        hash_sha512 = hashlib.sha512()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
        return hash_sha512.hexdigest()


    def calculaHashes(self):
        erros = []
        Arq = io.StringIO()
        # ArqHashdoHash = io.StringIO()
        lista_arquivos = self.listarArquivos(self.directory)
        with tqdm(total=len(lista_arquivos)) as pbar:
            for count, item in enumerate(lista_arquivos):
                try:
                    Arq.write(self.sha512(item) + '  ' + item.replace(self.directory + '\\', "").replace('\\', '/'))
                    # progress(count + 1, total)
                    pbar.update(1)
                    Arq.write('\n')
                except:
                    try:
                        Arq.write(
                            self.sha512(item) + '  ' + item.replace(self.directory + '\\', "").replace('\\', '/'))
                        Arq.write('\n')
                    except:
                        erros.append("\nErro no arquivo: " + str(item))
        Arq.seek(0)
        with codecs.open(os.path.join(self.directory, NomeDoArquivoHash), 'w', encoding='utf-8') as f:
            f.write(Arq.read())

    def calculaHashDoHash(self):
        HashdoHash = self.sha512(os.path.join(self.directory, NomeDoArquivoHash)).strip()
        with codecs.open(os.path.join(self.directory_hash_hash, NomeDoArquivoHashdoHash), 'w', encoding='utf-8') as f:
            f.write(HashdoHash)
        print("\nO hash do hash é: ")
        print("\n" + HashdoHash)
    
if __name__ == "__main__":
    hasher = Hasher()
    hasher.directory = r'C:\Users\renato\Desktop\temp\teste_report\Motorola'
    hasher.directory_hash_hash = r'C:\Users\renato\Desktop\temp\teste_report'
    hasher.calculaHashes()
    hasher.calculaHashDoHash()
