from PyQt5.QtCore import QThread, pyqtSignal
from waitress import serve
from app import app

class ServerThread(QThread):
    # signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.port = 5000
        
    # run method gets called when we start the thread
    def run(self):
        serve(app, host='0.0.0.0', port=self.port)
        self.ui.led_url.setText(f"http://localhost:5000")