from pathlib import Path
import os


app_dir = Path(os.path.dirname(os.path.realpath(__file__)))
sinftools_dir = Path(os.getenv("SINFTOOLS"))
jarfile = app_dir / "ipedexport-1.0-SNAPSHOT.jar"