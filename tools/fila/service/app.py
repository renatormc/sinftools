from flask import Flask
from api import api
from sinf.servers.database import db_session
from scheduler import scheduler, SchedulerConfig

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object(SchedulerConfig())
scheduler.init_app(app)
scheduler.start()

app.register_blueprint(api)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)