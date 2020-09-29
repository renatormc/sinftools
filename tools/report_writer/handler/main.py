import argparse
from handler import Handler

parser = argparse.ArgumentParser(description='Handle libreoffice.')
parser.add_argument('command', type=str,  help='Command')


args = parser.parse_args()
handler = Handler()
handler.connect()
if args.command == "compile":
    handler.compile()
elif args.command == "replace":
    handler.replace_vars()