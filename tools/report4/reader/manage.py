import sys
import os
import shutil
import settings
from pathlib import Path
sinftools_dir = os.getenv("SINFTOOLS")

def build(*args):
    os.system(f"s-pyinstaller --noconsole --hidden-import sqlalchemy.ext.baked --hidden-import PyQt5.sip --hidden-import inflection --paths \"{sinftools_dir}\\extras\\Python\\Lib\\site-packages\\PyQt5\\Qt\\bin\" --add-data \"templates;templates\" --add-data \"static;static\" --add-data \"reader_server\\resources;reader_server\\resources\" --add-data \"report_docx\\templates;report_docx\\templates\"  gui_server.py")
    pfrom = Path(f"{sinftools_dir}/Miniconda3/Lib/site-packages/PyQt5/Qt/bin")
    pto = settings.app_dir / "dist/gui_server/PyQt5/Qt/bin"
    shutil.rmtree(pto)
    shutil.copytree(pfrom, pto)
  
locals()[sys.argv[1]](*sys.argv[1:])