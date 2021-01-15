from pathlib import Path


def is_iped_results_folder(folder):
    folder = Path(folder)
    if not folder.name == "indexador":
        return False
    if not (folder / "IPEDConfig.txt").exists() or not (folder / "index").exists() or not (folder / "conf").exists() or not (folder / "subitens").exists() or not (folder / "jre").exists():
        return False
    return True
