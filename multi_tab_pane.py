from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout, QTabWidget, QTableView, QWidget
from tab_content_view import TabContentView

class MultiTabPane(QWidget):

    def __init__(self, parent=None) -> None:
        super(MultiTabPane, self).__init__(parent)
        self.setup_ui()
        self.tab_widget = QTabWidget(self)
        self.vertical_layout_center.addWidget(self.tab_widget)

    def setup_ui(self):
        self.resize(400, 300)
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setContentsMargins(11, 11, 11, 11)
        line_edit_top = QLineEdit(self)
        line_edit_top.setReadOnly(True)

        vertical_layout.addWidget(line_edit_top)

        self.vertical_layout_center = QVBoxLayout()
        self.vertical_layout_center.setSpacing(6)

        vertical_layout.addLayout(self.vertical_layout_center)

        line_edit_bottom = QLineEdit(self)
        line_edit_bottom.setReadOnly(True)

        vertical_layout.addWidget(line_edit_bottom)


    def add_tab(self, path: str) -> None:
        tab_content_view = TabContentView(self)
        self.tab_widget.addTab(tab_content_view, "")
        tab_content_view.set_path(path)

    def set_current_tab_index(self, index: int):
        if(index < 0 or index >= self.tab_widget.count()):
            return
        self.tab_widget.setCurrentIndex(index)


