from pathlib import Path
from sinf.servers import config
from datetime import datetime
import jwt
from sinf.servers.exceptions import TokenNoFoundException, TokenExpiredException

def get_acess_token():
    path = config.sinftools_dir / "var/sinftoken"
    if not path.exists():
        raise TokenNoFoundException("Para maior segurança o acesso remoto aos servidores exigem um token de acesso, que não foi encontrado em sua máquina. \nAcesse o Sinfweb no menu \"Usuário\" para obter seu token de acesso.")
    now = datetime.now()
    token = path.read_text(encoding="utf-8")
    headers = jwt.get_unverified_header(token)
    try:
        if headers['exp'] < datetime.timestamp(now):
            raise TokenExpiredException("Token expirado. Acesse o Sinfweb no menu \"Usuário\" para um novo.")
    except KeyError:
        pass
    return token