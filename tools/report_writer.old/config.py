from pathlib import Path
import os

from tempfile import gettempdir

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))

try:
    from sinf.sinftools_config import SinfToolsConfig
    stc = SinfToolsConfig()

    if os.name == 'nt':
        libreoffice_python = stc.getprop('laudos.libreoffice_python') or "C:\\Program Files\\LibreOffice\\program\\python.exe"
    else:
        libreoffice_python = stc.getprop('laudos.libreoffice_python') or "/usr/bin/python3"
    libreoffice_python = Path(libreoffice_python)
    printer_name = stc.getprop('laudos.printer_name') or "SINF"
    contexto_local = stc.getprop('laudos.contexto_local') or {'relator': "XXXX"}
except ImportError:
    pass

workdir = Path(".")
pics_folder = workdir / "fotos"
laudo_file = workdir / "laudo.odt"
capa_file = workdir / "capa.odt"
midias_file = workdir / "midia.odt"
data_file = workdir / "data.ods"
tempdir = Path(gettempdir()) / "report_writer"
if not tempdir.exists():
    tempdir.mkdir()
context_file = tempdir / "context.json"
print(f"Context File: {context_file}")
# context_file = Path("./context.json")
subdocs_temp_dir = tempdir / "subdocs"


numbering_items = {
    'pic': "Foto"
}


