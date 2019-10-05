from PySide2.QtWidgets import QTableView, QHeaderView
from PySide2.QtCore import Qt
from folder_model import FolderModel

class TabContentView(QTableView):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        print("TabContentView.__init__")
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
        print("TabContentView.set_path(%s)" %(path))
        self.clearSelection()
        self._folder_model.set_root_path(path)

