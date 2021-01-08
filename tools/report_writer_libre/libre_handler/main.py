import argparse
from uno_handler import UnoHandler

parser = argparse.ArgumentParser()
parser.add_argument('command')

args = parser.parse_args()
if args.command == "test":
    print("Test")
