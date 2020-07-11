import os
from pathlib import Path

sinftools_dir = Path(os.getenv("SINFTOOLS"))
MONGO_URI = "mongodb://localhost/test"
PASTA_ARQUIVOS = Path("C:/temp/casos")