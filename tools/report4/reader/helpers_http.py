from flask import url_for, session
from uuid import uuid4
import json
import settings

def url_for_local(path):
    if not path:
        path = settings.unknow_avatar

    url = url_for('ajax.workdir', relative_path=path)
    return f"{url}#{random_id()}"


def random_id():
    return str(uuid4()).replace("-", "")

def get_json_payload(request):
    return json.loads(request.form['payload'])


