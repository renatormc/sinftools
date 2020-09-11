import os
from pathlib import Path

sinftools_dir = Path(os.getenv("SINFTOOLS"))
app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
port = 8010
upload_folder = Path("./upload")