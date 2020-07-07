from PyQt5.QtCore import QThread, QEventLoop, QTimer, pyqtSignal
import config
from database import db_connect, db_session
from helpers.process_manager import ProcessManager


class Scheduler(QThread):
    updated = pyqtSignal()

    def __init__(self, standalone, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.standalone = standalone
        self.dataCollectionTimer = QTimer()
        self.dataCollectionTimer.moveToThread(self)
        self.dataCollectionTimer.timeout.connect(self.periodic)
        self.paused = False

      
    def periodic(self):
        pm = ProcessManager(db_session)
        pm.check_process()
        self.updated.emit()
      

    def run(self):
        self.dataCollectionTimer.start(config.fila_interval_check)
        loop = QEventLoop()
        loop.exec_()
