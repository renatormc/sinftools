from pathlib import Path
import os

sinftools_dir = Path(os.getenv("SINFTOOLS"))

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))