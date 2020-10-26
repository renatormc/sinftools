import config
from pathlib import Path
import subprocess
import questions


def read_items(path: Path):
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    items = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            items.append(line)
    return items


def categories2query(write_file=True):
    path = Path(".ipedexport/categoriesToExport.txt")
    categories = read_items(path)
    conditions = []
    for cat in categories:
        if " " in cat:
            aux = [item.strip() for item in cat.split(" ")]
            if len(aux) == 2:
                conditions.append(
                    f"(categoria:{aux[0]}* AND categoria:*{aux[1]})")
        else:
            conditions.append(f"categoria:{cat}")
    if write_file:
        aux = " OR ".join(conditions)
        query = f"isDir:false AND ({aux})"
        path = Path(".ipedexport/query.txt")
        path.write_text(query, encoding="utf-8")
    return conditions


def types2query(write_file=True):
    path = Path(".ipedexport/typesToExport.txt")
    types = read_items(path)
    conditions = []
    for type_ in types:
        conditions.append(f"tipo:{type_}")
    if write_file:
        aux = " OR ".join(conditions)
        query = f"isDir:false AND ({aux})"
        path = Path(".ipedexport/query.txt")
        path.write_text(query, encoding="utf-8")
    return conditions


def cattype2query():
    cat_cond = categories2query(write_file=False)
    type_cond = types2query(write_file=False)
    conditions = cat_cond + type_cond
    aux = " OR ".join(conditions)
    query = f"isDir:false AND ({aux})"
    path = Path(".ipedexport/query.txt")
    path.write_text(query, encoding="utf-8")


def run_export():
    args = ['java', '-jar', str(config.jarfile.absolute())]
    subprocess.run(args)


def build_query():
    res = questions.choose_filter()
    if res == "categories":
        categories2query()
    elif res == "types":
        types2query()
    elif res == "cat_type":
        cattype2query()
    elif res == "query":
        pass
