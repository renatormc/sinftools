from pathlib import Path
import os
from sinf.sinftools_config import SinfToolsConfig

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))

local_config = SinfToolsConfig()