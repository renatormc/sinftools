import argparse
from handler.handler import Handler

parser = argparse.ArgumentParser(description='Handle libreoffice.')
parser.add_argument('command', type=str,  help='Command')
parser.add_argument('-p', '--printer', dest='printer', action='store',
                     default="SINF",  help='Printer to be used')


args = parser.parse_args()
handler = Handler()
handler.connect()
if args.command == "compile":
    handler.compile()
elif args.command == "replace":
    handler.replace_vars()
elif args.command == "scan_pics":
    handler.scan_pics()
elif args.command == "read_calc":
    handler.read_calc()
elif args.command == "print":
    while True:
        value = input("Quantidade de cópias: ")
        try:
            n_copies = int(value)
            break
        except:
            pass
    value = input("Imprimir anexo de mídias? (s/N)")
    medias = value.lower() == "s"
    handler.print_all(args.printer, n_copies=n_copies, print_media=medias)