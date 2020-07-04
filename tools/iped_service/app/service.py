import waitress
from app import app
import os
import config
script_dir = os.path.dirname(os.path.realpath(__file__))

waitress.serve(app, host='0.0.0.0', port=8001)