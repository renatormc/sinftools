from ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from models import *
from pathlib import Path
from scanner import Scanner
from PyQt5.QtCore import Qt, QThread
import os
import markers
import config
from disk_dialog import DiskDialog
from case_dialog import CaseDialog
from hash_partial_dialog import HashPartialDialog

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




class MainWindow(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connections()
        self.ui.led_folder.setText(str(Path(".").absolute()))
        self.model2 = CaseFoldersModel()
        self.ui.tbv_table2.setModel(self.model2)
        self._what = "markers"
        self.setWindowIcon(QIcon(f"{config.app_dir}\\resources\\marker.png"))
        

    def connections(self):
        self.ui.btn_choose_folder.clicked.connect(self.choose_dir)
        self.ui.btn_find_markers.clicked.connect(self.find_markers)
        # self.ui.btn_open_folder.clicked.connect(self.open_folder)
        self.ui.tbv_table1.doubleClicked.connect(self.table1_double_click)
        self.ui.tbv_table2.doubleClicked.connect(self.table2_double_click)
        self.ui.btn_find_cases.clicked.connect(self.find_cases)
        self.ui.tbv_table1.clicked.connect(self.show_case_folders)
        self.ui.btn_mark_folder.clicked.connect(self.mark_folder)

    @property
    def folder(self):
        return Path(self.ui.led_folder.displayText())

    @property
    def what(self):
        return self._what

    @what.setter
    def what(self, value):
        self._what = value

    
    def set_buttons_enabled(self, value):
        self.ui.btn_mark_folder.setEnabled(value)
        self.ui.btn_find_markers.setEnabled(value)
        self.ui.btn_find_cases.setEnabled(value)

    def table1_double_click(self, index):
        if self.what == "markers":
            marker = self.model1.data(index, Qt.UserRole)
            markers.edit_markers(marker['folder'])
        # elif self.what == "cases":
        #     items =  self.model1.data(index, Qt.UserRole)['markers']
        #     self.model2.set_markers(items)
    
    def table2_double_click(self, index):
        if self.what == "cases":
            marker = self.model2.data(index, Qt.UserRole)
            os.system(f"explorer \"{marker['folder']}\"")

    def show_case_folders(self):
        if self.what == "cases":
            index = self.ui.tbv_table1.currentIndex()
            if index:
                items =  self.model1.data(index, Qt.UserRole)['markers']
                self.model2.set_markers(items)
            else:
                self.model2.clear()
        
    def mark_folder(self):
        type_ = self.ui.cbx_type.currentText()
        if type_ == "disk":
            dialog = DiskDialog(self.folder)
            dialog.exec_()
        elif type_ == "case":
            dialog = CaseDialog(self.folder)
            dialog.exec_()
        elif type_ == "hash_partial":
            dialog = HashPartialDialog(self.folder)
            dialog.exec_()

    # def open_folder(self):
    #     indexes = self.ui.tbv_table1.selectionModel().selectedRows()
    #     if indexes:
    #         self.model.data()

    def choose_dir(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Escolher diretório", str(self.folder))
        if directory:
            self.ui.led_folder.setText(str(Path(directory).absolute()))

    def print_status_bar(self, message):
        self.statusBar().showMessage(message)

    def add_marker(self, marker):
        item = QListWidgetItem(str(marker))

    
        # self.ui.tbv_table1.refresh()

    
    

    def find_markers(self):
        self.what = "markers"
        self.model1 = MarkersModel()
        self.ui.tbv_table1.setModel(self.model1)
        self.scanner = Scanner()

        def onfinish():
            self.set_buttons_enabled(True)

        def marker_found(marker):
            self.model1.markers.append(marker)
            self.model1.layoutChanged.emit()

        self.scanner.max_depth = self.ui.spb_depth.value()
        self.thread = QThread()
        
        self.thread.started.connect(self.scanner.find_markers)
        self.scanner.moveToThread(self.thread)
    

        self.scanner.new_marker_found.connect(marker_found)  
        self.scanner.print_message.connect(self.statusBar().showMessage)
        self.set_buttons_enabled(False)
        self.model1.markers = []
        self.thread.finished.connect(onfinish)
        self.scanner.finished.connect(self.thread.quit)
        self.thread.start()


    def find_cases(self):
        self.what = "cases"
        self.model1 = CasesModel()
        self.ui.tbv_table1.setModel(self.model1)
        self.scanner = Scanner()

        def onfinish():
            self.set_buttons_enabled(True)

        def marker_found(marker):
            if marker['type'] == 'case':
                self.model1.add_marker(marker)
            

        self.scanner.max_depth = self.ui.spb_depth.value()
        self.thread = QThread()
        
        self.thread.started.connect(self.scanner.find_markers)
        self.scanner.moveToThread(self.thread)
    

        self.scanner.new_marker_found.connect(marker_found)  
        self.scanner.print_message.connect(self.statusBar().showMessage)
        self.set_buttons_enabled(False)
        self.model1.clear()
        self.thread.finished.connect(onfinish)
        self.scanner.finished.connect(self.thread.quit)
        self.thread.start()
        


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
