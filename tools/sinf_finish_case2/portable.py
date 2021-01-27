from pathlib import Path
import sqlite3
import config
import os


class PortableHandler:

    def __init__(self):
        pass

    def find_image(self, directory, name, depth):
        if depth > config.max_depth:
            return
        name = name.lower()
        for entry in directory.iterdir():
            if entry.is_dir():
                return self.find_image(entry, name, depth + 1)
            elif entry.name.lower() == name:
                return entry

    def put_portable(self, folder: Path, depth=2):
        sleuth_path = folder / "sleuth.db"
        if sleuth_path.exists():
            conn = sqlite3.connect(str(sleuth_path))
            cursor = conn.cursor()
            cursor.execute("SELECT name, sequence FROM tsk_image_names;")
            for row in cursor.fetchall():
                path = Path(row[0])
                image_path = self.find_image(folder.parent, path.name, 0)
                if not image_path:
                    raise Exception(
                        f"O arquivo \"{path.name}\" não foi encontrado.")
                # rel_path = image_path.absolute().relative_to((folder).absolute())
                rel_path = os.path.relpath(image_path, folder)
                cursor.execute(
                    "UPDATE tsk_image_names SET name = ? WHERE sequence = ?", (rel_path, row[1]))
            conn.commit()
            conn.close()
