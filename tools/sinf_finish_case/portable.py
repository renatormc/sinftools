from pathlib import Path
import sqlite3
import sys
import config


def find_image(directory, name):
    for entry in directory.iterdir():
        if entry.is_dir():
            res = find_image(entry, name)
            if res:
                return res
        elif entry.name.lower() == name.lower():
            return entry


def put_portable(folder: Path):
    sleuth_path = folder /  "sleuth.db"
    if sleuth_path.exists():
        print(f"Tornando pasta \"{folder.absolute()}\" portable.")
        conn = sqlite3.connect(str(sleuth_path))
        cursor = conn.cursor()
        cursor.execute("SELECT name, sequence FROM tsk_image_names;")
        for row in cursor.fetchall():
            path = Path(row[0])
            image_path = find_image(folder.parent / config.EXTRACTION_FOLDER_NAME, path.name)
            if not image_path:
                raise Exception(f"O arquivo \"{path.name}\" não foi encontrado.")
            rel_path = image_path.absolute().relative_to((folder / config.EXTRACTION_FOLDER_NAME).absolute())
            new_path = f"..\\{config.EXTRACTION_FOLDER_NAME}\\{rel_path}"
            cursor.execute("UPDATE tsk_image_names SET name = ? WHERE sequence = ?", (new_path, row[1]))
        conn.commit()
        conn.close()
