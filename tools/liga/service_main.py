import waitress
from service.app import app
import os
import sys
import config
script_dir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) > 1 and sys.argv[1] == "dev":
    app.run(host='0.0.0.0', port=config.service_port, debug=True)
else:
    waitress.serve(app, host='0.0.0.0', port=config.service_port)