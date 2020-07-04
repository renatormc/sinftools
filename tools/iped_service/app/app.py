from flask import Flask
from api import api
from database import db_session

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(api)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)