from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig

stc = SinfToolsConfig()

sinftools_dir = Path(os.getenv("SINFTOOLS"))
app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
if os.name == 'nt':
    libreoffice_python = stc.getprop('laudos.libreoffice_home') or "C:\\Program Files\\LibreOffice"
else:
    libreoffice_python = stc.getprop('laudos.libreoffice_python') or "/usr/bin/python3"
libreoffice_python = Path(libreoffice_python)
printer_name = stc.getprop('laudos.printer_name') or "SINF"
contexto_local = stc.getprop('laudos.contexto_local') or {'relator': "XXXX"}

