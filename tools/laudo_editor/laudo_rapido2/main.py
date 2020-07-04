import os
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QStyleFactory, QPushButton, QStyleFactory, QScrollArea, QListWidgetItem, QComboBox, QHBoxLayout, QLabel, QMainWindow, QAction, QLineEdit
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from helpers import get_items
from PyQt5.QtCore import Qt
# import qdarkstyle
from fill import WindowFill
import settings
# from analise_template import analise
from helpers import prepare_env


class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setup_ui()
        self.connections()
        prepare_env()

    def setup_ui(self):
        self.setWindowIcon(
            QIcon(os.path.join(settings.app_dir, "resources", "notebook.png")))
        self.setWindowTitle("Laudo rápido 2")
        self.main_layout = QVBoxLayout()
        self.central_widget = QWidget()

        self.led_find = QLineEdit()
        self.led_find.setPlaceholderText("Filtrar modelos")
        self.led_find.placeholderText()

        self.lsw_items = QListWidget()

        self.main_menu = self.menuBar()

        self.modelos_layout = QHBoxLayout()

        self.populate_items()

        self.file_menu = self.main_menu.addMenu('Arquivo')
        self.open_models_folder_action = QAction(
            'Abrir pasta de meus modelos', self)
        self.file_menu.addAction(self.open_models_folder_action)

        self.main_layout.addWidget(self.led_find)
        self.main_layout.setStretch(0, 0)

        self.main_layout.addWidget(self.lsw_items)
        self.main_layout.setStretch(1, 0)

        self.scrool_area = QScrollArea()

        self.main_layout.addWidget(self.scrool_area)
        self.main_layout.setStretch(2, 3)

        self.window_fill = None

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

    def connections(self):
        self.lsw_items.itemDoubleClicked.connect(self.select_item)
        self.open_models_folder_action.triggered.connect(
            self.open_folder_models)
        self.led_find.textChanged.connect(self.filter_models)

    def filter_models(self):
        for i in range(self.lsw_items.count()):
            item = self.lsw_items.item(i)
            if self.led_find.displayText().lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def populate_items(self):
        self.lsw_items.clear()
        self.items = get_items()
        for item in self.items:
            new_item = QListWidgetItem()
            new_item.setText(item['name'])
            new_item.setData(Qt.UserRole, item)
            self.lsw_items.addItem(new_item)

    def select_item(self):
        data = self.lsw_items.currentItem().data(Qt.UserRole)
        if self.window_fill is not None:
            self.window_fill.deleteLater()
        self.window_fill = WindowFill(data)
        # self.window_fill.setFixedWidth(int(0.9*self.width()))
        self.scrool_area.setWidget(self.window_fill)
        self.scrool_area.setWidgetResizable(True)

    # def open_doc(self):
    #     os.system(f"start {settings.app_dir}\\doc\\doc.pdf")

    def open_folder_models(self):
        os.system(f"explorer {settings.app_user_folder}")


if __name__ == "__main__":
    n = len(sys.argv)

    if n > 1 and sys.argv[1] == 'reset':
        prepare_env(reset=True)
    else:
        app = QApplication(sys.argv)
        app.setStyle(QStyleFactory.create('fusion'))
        w = Window()
        w.setGeometry(300, 50, 900, 900)
        w.show()
        sys.exit(app.exec_())
