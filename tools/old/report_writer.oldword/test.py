import re

reg = re.compile(r'\{\{\s*(\S{1,15}\s*)\}\}')
res = reg.search("{{ testesdfffdfgggggggggggggg }}")
print(res.group(1))