import subprocess
import os
from pathlib import Path
import re
import sys

sinftools_dir = Path(os.getenv("SINFTOOLS"))
ftkimager_path = sinftools_dir / "extras/ftkimager/ftkimager.exe"

cmd = [str(ftkimager_path), "--list-drives"]

process = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

out, err = process.communicate()
text = err.decode("CP850")

lines = text.split("\n")
items = [line.strip() for line in lines if line.strip().startswith("\\\\")]
print(items)
# s-ftkimager \\.\PHYSICALDRIVE4 "D:\path\to\image\hdd" --e01 --verify