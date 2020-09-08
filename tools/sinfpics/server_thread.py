from PyQt5.QtCore import QThread, pyqtSignal
from waitress import serve
from app import app
import config

class ServerThread(QThread):
    # signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        
        
    # run method gets called when we start the thread
    def run(self):
        serve(app, host='0.0.0.0', port=config.port)
        