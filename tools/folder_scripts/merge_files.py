import os
import sys

n = len(sys.argv)
if n < 4:
    print("Quantidade de argumentos insuficientes")
    sys.exit()

files_in = [open(f, "rb") for f in sys.argv[1:n-1]]
file_out = open(sys.argv[n-1], 'wb')

for file in files_in:
    file_out.write(file.read())

for file in files_in:
    file.close()
file_out.close()

