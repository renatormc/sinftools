

from PyQt5.QtCore import QAbstractTableModel, QVariant, QModelIndex
from PyQt5.QtCore import Qt


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


class CasesModel(QAbstractTableModel):
    def __init__(self):
        super(CasesModel, self).__init__()
        self.cases = []
        self.casemap = {}

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.cases[index.row()]['name']
        elif role == Qt.UserRole:
            return self.cases[index.row()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "Caso"
        return QVariant()

    def rowCount(self, index):
        return len(self.cases)

    def columnCount(self, index):
        return 1

    def clear(self):
        self.cases= []
        self.casemap = {}

    def add_marker(self, marker):
        try:
            i = self.casemap[marker['name']]
            self.cases[i]['markers'].append(marker)
        except KeyError:
            self.cases.append({'name': marker['name'], 'markers':[marker]})
            self.casemap[marker['name']] = len(self.cases) - 1
            self.layoutChanged.emit()


class CaseFoldersModel(QAbstractTableModel):
    def __init__(self):
        super(CaseFoldersModel, self).__init__()
        self.markers = []
        self._colmap = {
            0: ('folder', 'Folder'),
            1: ('role', 'Role')

        }

    def set_markers(self, markers):
        self.markers = markers
        self.layoutChanged.emit()

    def clear(self):
        self.markers = []
        self.layoutChanged.emit()

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
