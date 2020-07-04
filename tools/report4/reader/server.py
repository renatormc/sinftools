from waitress import serve
from app import app
import socket
import sys
from ruamel.yaml import YAML
from pathlib import Path


def get_available_port():
    port = 5000
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            port += 1
            continue
        return port


def get_host_port():
    yaml = YAML()
    with Path('.report/config/config.yaml').open("r", encoding="utf8") as f:
        data = yaml.load(f.read())
    return data['online']['host'], data['online']['port']


def run(mode):
    port = get_available_port()
    if mode == 'debug':
        app.jinja_env.auto_reload = True
        app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
    elif mode == 'online':
        host, port = get_host_port()
        serve(app, host=str(host), port=int(port))
    elif mode == 'waitress':
        serve(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    run(sys.argv[1])
