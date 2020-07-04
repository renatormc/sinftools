import subprocess
import os
from pathlib import Path
import re
import sys

sinftools_dir = Path(os.getenv("SINFTOOLS"))
ftkimager_path = sinftools_dir / "extras/ftkimager/ftkimager.exe"

cmd = [str(ftkimager_path), "--list-drives"]

# cmd = ['dir']
process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

out, err = process.communicate()
text = err.decode("CP850")

identifier = sys.argv[1].strip()
if not identifier in text:
    print("Discos existentes")
    print(f"O disco \"{identifier}\" não foi encontrado.")
    sys.exit(1)
