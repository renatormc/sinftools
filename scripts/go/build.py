import subprocess
from pathlib import Path
import sys
import os

sinftools_dir = Path(os.getenv("SINFTOOLS"))

path = Path(sys.argv[1])
icopath = path.with_suffix(".ico")
exepath = sinftools_dir / "scripts" / path.with_suffix(".exe").name
args = ['go', 'build', '-ldflags', '-H=windowsgui', '-o', str(exepath), str(path)]
subprocess.run(args)

if icopath.exists():
    args = ['cmd', '/c', 'ResourceHacker.bat', '-open', str(exepath), '-save', str(exepath), '-action', 'addskip', '-res', str(icopath), '-mask', 'ICONGROUP,MAIN,' ]
    subprocess.run(args)
