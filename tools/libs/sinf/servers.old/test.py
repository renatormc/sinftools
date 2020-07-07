import config
from pathlib import Path
import sys
import re


path = config.app_dir / "conferir.txt"

with path.open("rb") as f:
    data = f.read()



# lines = data.split(b"\r\n")
# print(len(lines))
# lines = [line.split(b"\r")[-1] for line in lines]
# data = b"\r\n".join(lines)

path2 = config.app_dir / "conferir2.txt"
with path2.open("wb") as f:
    last_lf = None
    for i, b in enumerate(data):
        if b == b'\n':
            last_lf = i
        elif b == b'\r' and last_lf is not None:
            f.seek(last_lf)
        f.write(bytes(b))

# path2 = config.app_dir / "conferir2.txt"
# path2.write_text(text)
