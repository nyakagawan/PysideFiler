from PySide2.QtWidgets import QTableView, QFileSystemModel, QHeaderView
from PySide2.QtCore import Qt, QSortFilterProxyModel, QDir, QModelIndex, QFileInfo
from PySide2.QtGui import QBrush, QColor

import os
class Utility:
    @classmethod
    def is_windows(cls):
        return os.name == 'nt'

class FolderModel(QSortFilterProxyModel):
    ColumnFileName = 0
    ColumnFileType = 1
    ColumnFileSize = 2
    ColumnLastModified = 3

    def __init__(self, parent=None) -> None:
        self.setSortCaseSensitivity(Qt.CaseInsensitive)

        fs_model = QFileSystemModel(self)
        fs_model.setFilter(QDir.Filters.DEFAULT_FILTER_FLAGS)
        fs_model.rootPathChanged.connect(self.on_root_path_changed)
        fs_model.directoryLoaded.connect(self.on_root_path_changed)

        self.setSourceModel(fs_model)

    @property
    def fs_model(self) -> QFileSystemModel:
        return self.sourceModel()

    def on_root_path_changed(self, new_path: str):
        self.emit('rootPathChanged', new_path)

    def on_directory_loaded(self, path: str):
        self.emit('directoryLoaded', str)

    def columnCount(self, parent: QModelIndex) -> int:
        if(parent.column() > 0):
            return 0
        return 4

    def data(self, index:QModelIndex, role:int):
        if(not index.isValid()):
            return None

        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            fi = self.fs_model.fileInfo(index)
            if column == self.ColumnFileName:
                if Utility.is_windows() and fi.fileName() != '..' and self.is_drive(index):
                    return fi.absoluteFilePath()
                elif not fi.isDir() and not fi.completeBaseName() == '':
                    return fi.completeBaseName()
                else:
                    return fi.fileName()

            elif column == self.ColumnFileType:
                if not fi.isDir() and not fi.completeBaseName() == '':
                    return fi.suffix()

            elif column == self.ColumnFileSize:
                if Utility.is_windows():
                    return '<Drive>'
                elif fi.isDir():
                    return '<Folder>'
                else:
                    return fi.size()

            elif column == self.ColumnLastModified:
                return fi.lastModified().toString('yyyy-MM-dd HH:mm:ss')

            else:
                assert("unknown column")

        elif role == Qt.FontRole:
            raise NotImplemented

        elif role == Qt.TextAlignmentRole:
            if column == self.ColumnFileSize or column == self.ColumnLastModified:
                return Qt.AlignRight
            return Qt.AlignLeft

        elif role == Qt.TextColorRole:
            return self.get_text_brush()

        elif role == Qt.BackgroundRole:
            raise NotImplemented

        elif role == Qt.FileIconRole:
            raise NotImplemented

        elif role == Qt.FilePathRole:
            raise NotImplemented

        elif role == Qt.FileNameRole:
            raise NotImplemented


    def get_text_brush(self, index:QModelIndex) -> QBrush:
        # ret = QBrush()
        # fi = self.fs_model.fileInfo(index)
        return QBrush(QColor.fromRgb(0, 0, 0))

    def is_drive(self, index: QModelIndex):
        fi = self.fs_model.fileInfo(index)
        for drive in QDir.drives(): # type: QFileInfo
            if drive.absoluteFilePath() == fi.absoluteFilePath():
                return True
        return False


class TabContentView(QTableView):

    def __init__(self, parent=None) -> None:
        super(TabContentView, self).__init__(parent)
        self.setup_ui()

        self._folder_model = FolderModel(self)
        self._folder_model.fs_model.setReadOnly(True)
        self._folder_model.setDynamicSortFilter(True)
        self._folder_model.setSortLocaleAware(True)
        self.setModel(self._folder_model)

    def setup_ui(self):
        self.resize(400, 300)
        self.setGridStyle(Qt.SolidLine)
        self.setSortingEnabled(True)
        if not self.horizontalHeader().objectName():
            if not self.verticalHeader().objectName():
                self.verticalHeader().setVisible(False)

    def setModel(self, model: FolderModel):
        super().setModel(model)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def set_path(self, path: str):
        pass
