from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex
from pathlib import Path
from scanner import Scanner
from PyQt5.QtCore import Qt
import os
import markers

# class ListModel(QAbstractListModel):
#     def __init__(self, parent=None, *args):
#         """ datain: a list where each item is a row
#         """
#         QAbstractListModel.__init__(self, parent, *args)
#         self.markers = []

#     def addItem(self, item):
#         self.markers.append(item)

#     def rowCount(self, parent=QModelIndex()):
#         return len(self.markers)

#     def data(self, index, role):
#         if index.isValid() and role == Qt.DisplayRole:
#             return str(self.markers[index.row()])
#         else:
#             return None


class MarkersModel(QAbstractTableModel):
    def __init__(self):
        super(MarkersModel, self).__init__()
        self.markers = []
        self._colmap = {
            0: ('type', 'Type'),
            1: ('folder', 'Folder')
            
        }
     

    def data(self, index, role):
        if role == Qt.DisplayRole:
            key = self._colmap[index.column()][0]
            return self.markers[index.row()][key]
        elif role == Qt.UserRole:
            return self.markers[index.row()]
        
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._colmap[col][1]
        return QVariant()

    def rowCount(self, index):
        return len(self.markers)

    def columnCount(self, index):
        return 2


class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.ui.led_folder.setText(str(Path(".").absolute()))
        self.model = MarkersModel()
        self.ui.tbv_markers.setModel(self.model)

    def connections(self):
        self.ui.btn_choose_folder.clicked.connect(self.choose_dir)
        self.ui.btn_scan_all.clicked.connect(self.scan_drives)
        self.ui.btn_open_folder.clicked.connect(self.open_folder)
        self.ui.tbv_markers.doubleClicked.connect(self.table_double_click)

    @property
    def folder(self):
        return Path(self.ui.led_folder.displayText())

    def table_double_click(self, index):
        marker = self.model.data(index, Qt.UserRole)
        markers.edit_markers(marker['folder'])
        

    def open_folder(self):
        indexes = self.ui.tbv_markers.selectionModel().selectedRows()
        if indexes:
            self.model.data()

    def choose_dir(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Escolher diretório", str(self.folder))
        if directory:
            self.ui.led_folder.setText(str(Path(directory).absolute()))

    def print_status_bar(self, message):
        self.statusBar().showMessage(message)

    def add_marker(self, marker):
        item = QListWidgetItem(str(marker))

    def marker_found(self, marker):
        self.model.markers.append(marker)
        self.model.layoutChanged.emit()
        # self.ui.tbv_markers.refresh()

    def scan_drives(self):
        self.scanner = Scanner()
        self.scanner.max_depth = self.ui.spb_depth.value()

        def onfinish():
            self.ui.btn_scan_all.setEnabled(True)

        self.scanner.new_marker_found.connect(self.marker_found)
        self.scanner.finished.connect(onfinish)
        self.scanner.print_message.connect(self.statusBar().showMessage)
        self.ui.btn_scan_all.setEnabled(False)
        self.model.markers = []
        self.scanner.start()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
