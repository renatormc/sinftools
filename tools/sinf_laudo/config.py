from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))
stc = SinfToolsConfig()
printer_name = stc.getprop('laudos.printer_name') or "SINF"
printer_duplex_name = stc.getprop('laudos.printer_duplex_name') or "SINFDUPLEX"