from datetime import datetime
import json

d = datetime.now()
res = json.dumps(d)
print(res)
