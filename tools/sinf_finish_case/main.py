from hasher import Hasher
import argparse

parser = argparse.ArgumentParser(description='Finish case.')
parser.add_argument('-w', dest='n_workers', default=4, type=int, help='Number of workers')

args = parser.parse_args()


if __name__ == "__main__":
    hasher = Hasher(".")
    hasher.n_workers = args.n_workers
    hasher.run()