import subprocess
from pathlib import Path
import os
from shlex import quote
import pipes

sinftools_dir = Path(os.getenv("SINFTOOLS"))
python_exe = sinftools_dir / "extras/Python/python.exe"

def compile(path):
    path = Path(path)
    output = path.parent / f"ui_{path.stem}.py"
    args = [str(python_exe), "-m", "PyQt5.uic.pyuic", str(path), "-o", str(output)]
    subprocess.run(args)

compile(".\\main_window.ui")