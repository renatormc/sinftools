import config
import re
from subprocess import Popen
import os
import getpass


def parse_ip_port(str_):
    reg = re.compile(r'http://(.+):(\d+)')
    res = reg.search(str_)
    if res:
        ip, port = res.group(1), int(res.group(2))
    else:
        ip, port = None, None
    return ip, port


def connect_rdp(servername):

    if os.name == "nt":
        # Generate connection file
        template = config.app_dir / "cmdtool/connection_files/template.rdp"
        rdpfile = config.app_dir / "cmdtool/connection_files/rdpfile.rdp"
        text = template.read_text(encoding="utf-16-le")
        ip, port = parse_ip_port(config.servers[servername]['url'])
        text = text.replace("$server_ip", ip)
        rdpfile.write_text(text, encoding="utf-16-le")

        windir = os.getenv("windir")
        Popen(f"{windir}\\system32\\mstsc.exe \"{rdpfile}\"")
    else:
        ip, _ = parse_ip_port(config.servers[servername]['url'])
        p = getpass.getpass() 
        cmd = f"xfreerdp /u:sinf /v:{ip} /p:{p} +clipboard"
        Popen(cmd)
