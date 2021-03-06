from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig

sc = SinfToolsConfig()

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))

models_folder = app_dir / "models"

object_types = ['Celular', 'Computador', 'Notebook']

printer_name = sc.getprop("laudos.printer_name")


