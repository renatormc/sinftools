from pathlib import Path
import re


def is_iped_ignore(folder):
    folder = Path(folder)
    if folder.name != "indexador" \
            or not (folder / "IPEDConfig.txt").exists() \
            or not (folder / "index").exists() \
            or not (folder / "conf").exists() \
            or not (folder / "subitens").exists() \
            or not (folder / "jre").exists() \
            or (not (folder.parent / "FileList.csv").exists() and not (folder.parent / "Lista de Arquivos.csv").exists()):
        return False
    return True


def is_e01_partial(path: Path):
    if re.match(r'.*\.[Ee]0\d+$', path.name):
        first_fragment = path.with_suffix(".E01")
        log = first_fragment.parent / f"{first_fragment.name}.txt"
        print("easdf", log)
        if log.exists():
            print("Existe")
            return True
    return False