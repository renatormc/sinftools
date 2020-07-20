from pathlib import Path
import config
import markers
import hashlib
from portable import put_portable
import logging 

logging.basicConfig(filename="hash.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 

root = Path('.')
hash_file = root / "hash.txt"



def sha512(fname):
    if fname.endswith(".sinf_mark.json"):
        return
    print(f"Calculando hash de \"{fname}\"")
    hash_sha512 = hashlib.sha512()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha512.update(chunk)
    except (FileNotFoundError, OSError) as e:
        logger.error(str(e))

    return hash_sha512.hexdigest()


def is_iped_image_folder(folder: Path):
    markers_ = markers.get_markers_folder(folder)
    for marker in markers_:
        if marker and marker['type'] == "iped_image_folder":
            return True
    return False


def hash_iped_image_folder(folder, f):
    try:
        for item in folder.iterdir():
            if item.is_file() and item.suffix in [".log", ".txt"]:
                res = sha512(str(item))
                if res:
                    f.write(f"{res}     {item.relative_to(root)}\n")
            elif item.is_dir():
                if is_iped_image_folder(item):
                    hash_iped_image_folder(item, f)
                else:
                    hash_folder_not_iped(item, f)
    except (FileNotFoundError, OSError):
        logger.error(str(e))



def is_iped_folder(folder: Path):
    """Classifica uma pasta como sendo processamento do iped caso haja duas subpastas extracao e processamento"""
    return (folder / config.EXTRACTION_FOLDER_NAME).exists() and (folder / config.PROCESS_FOLDER_NAME).exists()


def hash_folder_not_iped(folder, f):
    try:
        for entry in folder.iterdir():
            if entry.is_dir():
                hash_folder_not_iped(entry, f)
            else:
                res = sha512(str(entry))
                if res:
                    f.write(f"{res}     {entry.relative_to(root)}\n")
    except (FileNotFoundError, OSError) as e:
        logger.error(str(e))


with hash_file.open("w", encoding="utf-8") as f:
    logger.info("Iniciando...")
    for entry in root.iterdir():
        if entry.is_file():
            continue
        print(f"Analisando pasta \"{entry}\"")
        if not is_iped_folder(entry):
            hash_folder_not_iped(entry, f)
        else:
            extraction_folder = entry / config.EXTRACTION_FOLDER_NAME
            if is_iped_image_folder(extraction_folder):
                hash_iped_image_folder(extraction_folder, f)
            else:
                hash_folder_not_iped(extraction_folder, f)
            item = entry / config.PROCESS_FOLDER_NAME / "FileList.csv"
            if not item.exists():
                item = entry / config.PROCESS_FOLDER_NAME / "Lista de Arquivos.csv"
            if item.exists():
                res = sha512(str(item))
                f.write(f"{res}     {item.relative_to(root)}\n")
        
            put_portable(entry)

res = sha512(str(root / hash_file))
print("Hash do hash")
print(res)
logger.info("Finalizou")
logger.info(f"Hash do hash: {res}")
