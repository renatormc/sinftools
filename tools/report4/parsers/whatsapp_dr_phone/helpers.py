import re

def parse_timestamp(line):
    res = re.search(r'<p class=\'date\'><font color=\'(.*)\'>Date: (.*)</font></p>', line)
    if res:
        value = res.group(2)
        return value
        
def parse_body(line):
    res = re.search(r'<p class=\'triangle-isosceles(.*?)\'><font color=\'(.*?)\'>(.*?)</font></p>', line)
    if res:
        value = (True, res.group(3)) if res.group(1) else (False, res.group(3))
        return value
    res = re.search(r'<p class=\'triangle-isosceles(.*?)\'>(.*?)</p>', line)
    if res:
       
        value = (True, res.group(2)) if res.group(1) else (False, res.group(2))
        return value
    
def parse_from(line):
    res = re.search(r'^<p><font color=\'(.*?)\'>(.*?)</font></p>$', line)
    if res:
        value = res.group(2)
        return value
    
def parse_chat_identifier(line):
    res = re.search(r'<p><img(.*?)/><h3 style=\'(.*?)\'>(.*?)</h3></p>', line)
    if res:
        value = res.group(3)
        return value
    
def parse_line(line):
    value = parse_timestamp(line)
    if value:
        return "timestamp", value
    value = parse_body(line)
    if value:
        return "body", value
    value = parse_chat_identifier(line)
    if value:
        return "chat_identifier", value
    value = parse_from(line)
    if value:
        return "from", value
    return None, None

