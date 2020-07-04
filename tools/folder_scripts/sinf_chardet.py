import chardet
import sys

rawdata = open(sys.argv[1], "r").read()
result = chardet.detect(rawdata)
charenc = result['encoding']
print(f"Detectado {charenc}")