import os
from pathlib import Path
import json
import sinf.servers.config as cf

sinftools_dir = Path(os.getenv("SINFTOOLS"))

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))


servers = cf.servers

secret_key = os.getenv("SINFKEY")

scripts_template = {
    "Processamento do IPED": {"script": "iped.bat", "process_type": "IPED"},
    "Imagem": {"script": "image.bat", "process_type": "Imagem"},
    "Outro": {"script": "other.bat", "process_type": "Outro"},
    "Sincronizar pastas": {"script": "synkdir.bat", "process_type": "Sincronização de pastas"}
}