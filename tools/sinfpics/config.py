import os
from pathlib import Path

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))
debug = True
url_sinfweb = "http://localhost:8000" if debug else "http://10.129.3.14"