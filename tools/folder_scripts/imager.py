import sys
import json
import codecs
import wmi
import argparse
import os
from datetime import datetime

parser = argparse.ArgumentParser(description='SINF Imager')
parser.add_argument('-a',  dest='action_', required=True, choices=['init', 'start', 'continue', 'list'])
parser.add_argument('--skip',  dest='skip', type=int, default=0)
args = parser.parse_args()


def save(config):
    with codecs.open("config.json", "w", "utf-8") as arq:
        arq.write(json.dumps(config, indent=2))

def loadconfig():
    with codecs.open("config.json", "r", "utf-8") as arq:
        return json.load(arq)

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben


def humanbytes(B):
   'Return the given bytes as a human friendly KB, MB, GB, or TB string'
   if not B:
       return ''
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

def init():
    info = getInfo()
    config = {
        "image_file": "",
        "drive": info[0],
        "size": info[1],
        "last_block": 0,
        "block_size": 512,
        "skip_blocks": []
    }
    
    config['image_file'] = input("Image file: ")
    config['block_size'] = int(input("Block size: "))
    save(config)

def getInfo(only_list=False):
    w = wmi.WMI()
    i = 0
    logical_drives = w.Win32_LogicalDisk()
    physical_drives = w.Win32_DiskDrive()
    print("----------------------------------------------------------------")
    for drive in physical_drives:
        i += 1
        print("{:<2d} | {:<20s} | {:<10s} | {}".format(i, drive.DeviceID, humanbytes(drive.Size), drive.Model))
        
    first_logical = i + 1

    for drive in logical_drives:
        i+= 1
        print("{:<2d} | {:<20s} | {:<10s} |".format(i, drive.Caption, humanbytes(drive.Size)))
    print("----------------------------------------------------------------")
    
    if not only_list:
        op = int(input("opção: "))
        retorno = {}
        if op > first_logical:
            drive = logical_drives[op - first_logical]
            retorno = (drive.Caption, int(drive.Size))
        else:
            drive = physical_drives[op -1]
            retorno = (drive.DeviceID, int(drive.Size))
    else:
        retorno = None
    return retorno
       

def read(config, start):
    qtd_blocks = int(int(config['size'])/config['block_size'])
    with open(config['drive'], 'rb') as f:
        with open(config['image_file'], 'ab') as fo:
            print("Iniciando leitura no bloco {}".format(start))
            last_prog = 0
            for i in range(start, qtd_blocks):
                config['last_block'] = i
                save(config)
                f.seek(i*config['block_size'])
                chunk = f.read(config['block_size'])
                fo.write(chunk)
                prog = int((i/qtd_blocks)*1000)
                if prog != last_prog:
                    last_prog = prog
                    print("{}% - {}".format(last_prog/10, datetime.now().strftime("%H:%M:%S")))
                # progress(i, qtd_blocks)
                
                
if args.action_ == "init":
    init()
elif args.action_ == "start":
    config = loadconfig()
    if os.path.exists(config['image_file']):
        os.remove(config['image_file'])
    config['last_block_ok'] = 0
    config['skip_blocks'] = []
    read(config, 0)
elif args.action_ == "continue":
    config = loadconfig()
    for i in range(config['last_block'], config['last_block'] + args.skip):
        config['skip_blocks'].append(i)
    read(config, config['last_block']  + args.skip)
elif args.action_ == "list":
    getInfo(only_list=True)



