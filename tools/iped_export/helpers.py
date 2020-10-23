import config
from pathlib import Path
import subprocess

def categories2query():
    path = Path(".ipedexport/categoriesToExport.txt")
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    categories = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            categories.append(line)
    conditions = []
    for cat in categories:
        if " " in cat:
            aux = [item.strip() for item in cat.split(" ")]
            if len(aux) == 2:
                conditions.append(f"(categoria:{aux[0]}* AND categoria:*{aux[1]})")
        else:
            conditions.append(f"categoria:{cat}")
    aux = " OR ".join(conditions)
    query = f"isDir:false AND ({aux})"
    path = Path(".ipedexport/query.txt")
    path.write_text(query, encoding="utf-8")


def run_export():
    args = ['java', '-jar', str(config.jarfile.absolute())]
    subprocess.run(args)


