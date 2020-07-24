
import sys

def print_safe(value, *args, **kargs):
    try:
        print(value, *args, **kargs)
    except UnicodeEncodeError:
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        print(value.translate(non_bmp_map), *args, **kargs)