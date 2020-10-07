import os
from pathlib import Path
import sys

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))
debug = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    print("Modo debug ligado")
    debug = True
url_sinfweb = "http://localhost:8000" if debug else "http://10.129.3.14"