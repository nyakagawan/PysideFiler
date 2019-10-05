from PySide2.QtWidgets import QFileSystemModel
from PySide2.QtCore import Qt, QSortFilterProxyModel, QDir, QModelIndex, QFileInfo, QItemSelectionModel, Signal
from PySide2.QtGui import QBrush, QColor, QIcon, QFont
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

    rootPathChagned = Signal(str)
    directoryLoaded = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._font = QFont()
        self._selection_model = QItemSelectionModel(self)
        self.setSortCaseSensitivity(Qt.CaseInsensitive)

        fs_model = QFileSystemModel(self)
        fs_model.setFilter(QDir.AllEntries | QDir.AccessMask | QDir.AllDirs | QDir.NoDot | QDir.NoDotDot)
        fs_model.rootPathChanged.connect(self.on_root_path_changed)
        fs_model.directoryLoaded.connect(self.on_root_path_changed)

        self.setSourceModel(fs_model)

    @property
    def fs_model(self) -> QFileSystemModel:
        return self.sourceModel()

    def on_root_path_changed(self, new_path: str):
        self.rootPathChagned.emit(new_path)

    def on_directory_loaded(self, path: str):
        self.directoryLoaded(path)

    def columnCount(self, parent: QModelIndex) -> int:
        if(parent.column() > 0):
            return 0
        return 4

    def fileInfo(self, index:QModelIndex) -> QFileInfo:
        return self.sourceModel().fileInfo(self.mapToSource(index))

    def data(self, index:QModelIndex, role:int):
        if(not index.isValid()):
            return super().data(index, role)

        column = index.column()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            fi = self.fileInfo(index)
            print(fi.filePath())
            if column == self.ColumnFileName:
                if Utility.is_windows():
                    if fi.fileName() != '..' and self.is_drive(index):
                        return fi.absoluteFilePath()

                if fi.isDir() and not fi.completeBaseName() == '':
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
            return self._font

        elif role == Qt.TextAlignmentRole:
            if column == self.ColumnFileSize or column == self.ColumnLastModified:
                return Qt.AlignRight
            return Qt.AlignLeft

        elif role == Qt.TextColorRole:
            return self.get_text_brush(index)

        elif role == Qt.BackgroundRole:
            return self.get_background_brush(index)

        elif role == QFileSystemModel.FileIconRole:
            if column == self.ColumnFileName:
                return self.fileIcon(index)

        elif role == QFileSystemModel.FilePathRole:
            if column == self.ColumnFileName:
                return self.filePath(index)

        elif role == QFileSystemModel.FileNameRole:
            if column == self.ColumnFileName:
                return self.fileName(index)

        # print("role=" + str(role))
        return super().data(index, role)

    def headerData(self, column:int, orientation:Qt.Orientation, role:int):
        if role == Qt.DisplayRole:
            if column == self.ColumnFileName:
                return "Name"
            if column == self.ColumnFileType:
                return "Type"
            if column == self.ColumnFileSize:
                return "Size"
            if column == self.ColumnLastModified:
                return "Last modified"

        return super().headerData(column, orientation, role)

    def is_selected(self, index:QModelIndex) -> bool:
        if not self._selection_model:
            return False
        return self._selection_model.isSelected(index)

    def get_background_brush(self, index:QModelIndex) -> QBrush:
        if self.is_selected(index):
            return QBrush(QColor.fromRgb(0, 0, 255))
        return QBrush(QColor.fromRgb(255, 255, 255))

    def get_text_brush(self, index:QModelIndex) -> QBrush:
        return QBrush(QColor.fromRgb(0, 0, 0))

    def set_root_path(self, path:str) -> QModelIndex:
        return self.mapFromSource(self.fs_model.setRootPath(path))

    def fileIcon(self, index:QModelIndex) -> QIcon:
        return self.fs_model.fileIcon(self.mapToSource(index))

    def filePath(self, index:QModelIndex) -> str:
        return self.fs_model.filePath(self.mapToSource(index))

    def fileName(self, index:QModelIndex) -> str:
        return self.fs_model.fileName(self.mapToSource(index))

    def is_drive(self, index: QModelIndex):
        fi = self.fileInfo(index)
        for drive in QDir.drives(): # type: QFileInfo
            if drive.absoluteFilePath() == fi.absoluteFilePath():
                return True
        return False

