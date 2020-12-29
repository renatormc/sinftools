from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig

stc = SinfToolsConfig()

sinftools_dir = Path(os.getenv("SINFTOOLS"))
app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
templates_dir = app_dir / "templates"
generated_laudo = Path("./laudo.docx")
excel_data_file = Path("./data.xlsx")
pics_folder = Path("./data/fotos")
