import waitress
from app import app
import os
script_dir = os.path.dirname(os.path.realpath(__file__))

waitress.serve(app, host='0.0.0.0', port=8002)
# app.run(host='0.0.0.0', port=8002, debug=True)