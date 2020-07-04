from pathlib import Path
from sinf.servers import markers
import sys
import json

data = []
max_depth = 5

root = Path(".")


with Path(sys.argv[1]).open("r", encoding="utf-8") as f:
    data = json.load(f)

for m in data:
    folder = Path(m['path'])
    print(f"Marcando diretório \"{m['path']}\"")
    markers.mark_folder(folder, m['marker'])