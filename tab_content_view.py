from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QTableView, QWidget, QSplitter, QSizePolicy, QLayout, QTextBrowser
import PySide2.QtCore

class TabContentView(QTableView):

    def __init__(self, parent=None) -> None:
        super(TabContentView, self).__init__(parent)

    def setup_ui(self):
        self.resize(400, 300)
        self.setGridStyle(PySide2.QtCore.Qt.SolidLine)
        self.setSortingEnabled(True)
        if not self.horizontalHeader().objectName():
            if not self.verticalHeader().objectName():
                self.verticalHeader().setVisible(False)

    def set_path(self, path: str):
        pass
