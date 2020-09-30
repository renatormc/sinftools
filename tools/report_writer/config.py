from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig

stc = SinfToolsConfig()

sinftools_dir = Path(os.getenv("SINFTOOLS"))
app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
libreoffice_home = stc.getprop('laudos.libreoffice_home') or "C:\\Program Files\\LibreOffice"
libreoffice_home = Path(libreoffice_home)
python_libre = libreoffice_home / "program/python.exe"
printer_name = stc.getprop('laudos.printer_name') or "SINF"
contexto_local = stc.getprop('laudos.contexto_local') or {'relator': "XXXX"}

