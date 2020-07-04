import shutil
import os
from pathlib import Path

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))
shutil.copy(script_dir / "Styles.docx", Path("./laudo.docx"))
