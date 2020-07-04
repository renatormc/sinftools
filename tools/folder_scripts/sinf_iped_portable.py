from pathlib import Path
import sqlite3
import sys

path = Path(".")


def find_image(directory, name):
    for entry in directory.iterdir():
        if entry.is_dir():
            res = find_image(entry, name)
            if res:
                return res
        elif entry.name == name:
            return entry


for entry in path.iterdir():
    sleuth_path = entry / "indexacao/sleuth.db"
    if entry.is_dir() and sleuth_path.exists():
        print(f"Alterando item {entry.name}")
        conn = sqlite3.connect(str(sleuth_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name, sequence FROM tsk_image_names;")
        for row in cursor.fetchall():
            path = Path(row[0])
            image_path = find_image(entry, path.name)
            if not image_path:
                print(f"Arquivo {path.name} não encontrado dentro da pasta \"imagem\"")
                sys.exit()
            rel_path = image_path.absolute().relative_to((entry / "imagem").absolute())
            new_path = f"..\\imagem\\{rel_path}"
            cursor.execute("UPDATE tsk_image_names SET name = ? WHERE sequence = ?", (new_path, row[1]))
        conn.commit()
        conn.close()
