from PyQt5.QtWidgets import *
from pics_dialog import PicsDialog
import json
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        w = QWidget(self)
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)

        self.btn_scan_pics = QPushButton("Scan Pics")
        self.btn_scan_pics.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_scan_pics.clicked.connect(self.scan_pics)
        self.main_layout.addWidget(self.btn_scan_pics)

    def scan_pics(self):
        self.pics_dialog = PicsDialog()
        if self.pics_dialog.exec_():
            data = self.pics_dialog.get_data()
            Path("objects.json").write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
