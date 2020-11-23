from pathlib import Path
import os

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))

config_file = sinftools_dir / "var/config/printers.json"