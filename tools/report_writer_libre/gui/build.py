import subprocess
from pathlib import Path
import os


sinftools_dir = Path(os.getenv("SINFTOOLS"))

def compile(path):
    path = Path(path)
    output = path.parent / f"ui_{path.stem}.py"
    args = ["s-py", "-m", "PyQt5.uic.pyuic", str(path), "-o", str(output)]
    subprocess.call(args)

compile("./gui/main_window.ui")