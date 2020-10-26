from flask import Flask
from database import db_session
from views import views
import jinja_filters as jinja_filters
import config


app = Flask(__name__)

app.secret_key = '!$%dfg'
app.register_blueprint(views)

for name, function in jinja_filters.__dict__.items():
    app.jinja_env.filters[name] = function


# @app.context_processor
# def context():
   
#     return dict(
      
#     )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=config.port, debug=True)