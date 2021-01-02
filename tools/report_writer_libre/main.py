from gui.main_window import MainWindow

import sys
from PyQt5.QtWidgets import QApplication
app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())