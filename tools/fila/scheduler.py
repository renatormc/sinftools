from PyQt5.QtCore import QThread, QEventLoop, QTimer, pyqtSignal
import config
from sinf.servers.database import db_connect, db_session
from sinf.servers.process_manager import ProcessManager


class Scheduler(QThread):
    updated = pyqtSignal()

    def __init__(self, standalone, *args, **kwargs):
        QThread.__init__(self, *args, **kwargs)
        self.standalone = standalone
        self.dataCollectionTimer = QTimer()
        self.dataCollectionTimer.moveToThread(self)
        self.dataCollectionTimer.timeout.connect(self.periodic)
        self.paused = False

 
    # def periodic(self):
    #     if self.standalone and not self.paused:
    #         engine, db_session = db_connect()
    #         try:
    #             pm = ProcessManager(db_session)
    #             pm.check_process()
    #             self.updated.emit()
    #         finally:
    #             engine.dispose()

    #     self.updated.emit()
      
    def periodic(self):
        pm = ProcessManager(db_session)
        pm.check_process()
        self.updated.emit()
      

    def run(self):
        self.dataCollectionTimer.start(config.interval_check)
        loop = QEventLoop()
        loop.exec_()
