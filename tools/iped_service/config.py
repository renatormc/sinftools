import os
from pathlib import Path
import json

sinftools_dir = Path(os.getenv("SINFTOOLS"))

app_dir = Path(os.path.dirname(os.path.realpath(__file__)))


servers = {
    'batman': {
        'url': "http://10.129.3.128:8001",
        'connection_file': app_dir / "connection_files/batman.rdp"
    },
    'superman': {
        'url': "http://10.129.3.132:8001",
        'connection_file': app_dir / "connection_files/superman.rdp"
    },
    'mulher_maravilha': {
        'url': "http://10.129.3.120:8001",
        'connection_file': app_dir / "connection_files/mulher_maravilha.rdp"
    }
}
