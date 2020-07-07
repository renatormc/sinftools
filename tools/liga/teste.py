import re

def parse_ip_port(str_):
    reg = re.compile(r'http://(.+):(\d+)')
    res = reg.search(str_)
    if res:
        ip, port = res.group(1), int(res.group(2))
    else:
        ip, port = None, None
    return ip, port

res = parse_ip_port("htt://10.129.3.14:8003/asdf")
# res = getipport("asdffff5df/*99")
print(res)