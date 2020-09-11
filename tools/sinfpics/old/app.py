from flask import Flask, request, jsonify, send_from_directory
import config
from flask_cors import CORS
import base64
from helpers import save_picture

app = Flask(__name__)
CORS(app)
sinf

@app.route("/")
def index():
    return "Hello world"


@app.route("/upload-pic", methods=("POST",))
def upload_pic():
    data = request.json
    encoded = data['base64'].split(",")[1]
    img = base64.b64decode(encoded)
    name = save_picture(img, data['name'])
    return name


@app.route("/pics")
def pics():
    files = [{'name': entry.stem, 'uri': f"pic/{entry.stem}"} for entry in config.upload_folder.iterdir(
    ) if entry.is_file() and entry.suffix == ".png"]
    return jsonify(files)


@app.route("/pic/<name>")
def pic(name):
    return send_from_directory(config.upload_folder, f"{name}.png")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.port, debug=True)
