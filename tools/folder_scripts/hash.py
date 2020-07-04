import sys
import os
import io
import codecs
import hashlib
import argparse
from sinf.hash import Hasher

parser = argparse.ArgumentParser(description='Calcula Hash de todos os arquivos dentro da pasta e gera o arquivo "hash.txt"')
parser.add_argument('-d', dest='diretorio', action='store', help='Diretório. Por default assume como sendo o corrente')
parser.add_argument('--hh', dest='somente_hash_hash', action='store_true', help='Somente calcular hash do hash.')
args = parser.parse_args()

hasher = Hasher()

if args.diretorio is not None:
    hasher.directory = args.diretorio
    hasher.directoy_hash_hash = os.path.join(args.diretorio, "..")
else:
    hasher.directory = "."
    hasher.directoy_hash_hash = ".."


if not args.somente_hash_hash:
    hasher.calculaHashes()
hasher.calculaHashDoHash()
# ArqHashdoHash.write(HashdoHash)

# ArqHashdoHash.seek(0)
# with open(os.path.join(config["Diretorio"], NomeDoArquivoHashdoHash), 'w') as f:
#     f.write(ArqHashdoHash.read())

input()