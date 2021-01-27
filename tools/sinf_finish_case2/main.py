from hasher import Hasher
import logging
import argparse
import config
import questions
import sys

parser = argparse.ArgumentParser(
    description='Calculates Sha512 checksum of file of files in a folder.')
parser.add_argument('-m', '--max-depth', type=int, default=2,
                    help='Max depth to search e01 files in order to make iped results portable in relation of sleuth.db parent folder.')
parser.add_argument('item', nargs='?', default=".", help='Directory or file to be hashed')

args = parser.parse_args()

config.max_depth = args.max_depth

hasher = Hasher()
hasher.root = args.item
if hasher.root.is_file():
    res = hasher.sha512(hasher.root, extra=True)
    print(res)
    sys.exit()

options = questions.get_options()
hasher.put_portable = options['put_portable']
hasher.images_partial = options['images_partial']
hasher.iped_partial = options['iped_partial']

logging.basicConfig(filename=str(hasher.log_file_path),
                    format='%(asctime)s %(message)s',
                    filemode='w')
hasher.count_files()
print(f"{hasher.total} arquivos encontrados.")
print("Iniciando cálculo de hashes.")
hasher.run()

