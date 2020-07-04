from sinf.hash_calc import HashCalc
from pathlib import Path

folder = Path(r'.')
hash_file = folder / "hash.txt"

hash_calc = HashCalc()


def find_log_hash(root, folder, f):
    for item in folder.iterdir():
        if item.is_file() and item.suffix in [".log", ".txt"]:
            res = hash_calc.sha512(str(item))
            f.write(f"{res}     {item.relative_to(root)}\n")
        elif item.is_dir():
            find_log_hash(item, f)

def is_iped_folder(folder):
    return (entry / "imagem").exists() and (entry / "indexacao").exists()

def hash_folder_not_iped(root, folder, f):
    for entry in folder.iterdir():
        if entry.is_dir():
            hash_folder_not_iped(root, entry, f)
        else:
            print(entry)
            res = hash_calc.sha512(str(entry))
            f.write(f"{res}     {entry.relative_to(root)}\n")

print("Para que o cálculo dos hashes funcione de forma correta é necessário que as pastas estejam estruturadas de forma que os processamentos do iped \ntenham as imagens em uma pasta de nome \"imagem\" e a indexação em uma pasta de nome \"idexacao\".")
input("Pressione alguma tecla para continuar...")

with hash_file.open("w", encoding="utf-8") as f:
    for entry in folder.iterdir():
        if entry.is_file():
            continue
        if not is_iped_folder(entry):
            hash_folder_not_iped(folder, entry, f)
        else:
            find_log_hash(folder, entry / "imagem", f)
            item = entry / "indexacao/FileList.csv"
            if not item.exists():
                item = entry / "indexacao/Lista de Arquivos.csv"
            if not item.exists():
                continue
            res = hash_calc.sha512(str(item))
            f.write(f"{res}     {item.relative_to(folder)}\n")

res = hash_calc.sha512(str(folder / hash_file))
print("Hash do hash")
print(res)
