from flask import Flask, request
import config
from flask_cors import CORS
import base64
from helpers import save_picture

app = Flask(__name__)
CORS(app)

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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.port, debug=True)