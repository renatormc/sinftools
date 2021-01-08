import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QLabel, QGridLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from pathlib import Path
from helpers import get_objects_from_pics


class HelloWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.dir = Path(".")
        self.setup_ui()
        self.load_objects()
        

    def setup_ui(self):
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Pics")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.main_layout = QVBoxLayout()
        centralWidget.setLayout(self.main_layout)

        

    def load_objects(self):
        objects = get_objects_from_pics("/media/renato/linux_data/laudos/AA/fotos")
        for obj in objects:
            layout = QHBoxLayout()
            for pic in obj['pics']:
                label = QLabel()
                pixmap = QPixmap(pic)
                label.setPixmap(pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                layout.addWidget(label)
            self.main_layout.addLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())
