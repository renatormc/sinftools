import re

def strfdatetime(value):
    if not value:
        return ""
    return value.strftime("%d/%m/%Y %H:%M:%S")

def parse_ip_port(str_):
    reg = re.compile(r'http://(.+):(\d+)')
    res = reg.search(str_)
    if res:
        ip, port = res.group(1), int(res.group(2))
    else:
        ip, port = None, None
    return ip, port