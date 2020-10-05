from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig
from tempfile import gettempdir

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

workdir = Path(".")
pics_folder = workdir / "fotos"
laudo_file = workdir / "laudo.odt"
capa_file = workdir / "capa.odt"
midias_file = workdir / "midia.odt"
data_file = workdir / "data.ods"
context_file = Path(gettempdir()) / "context.json"

numbering_items = {
    'pic': "Foto"
}


