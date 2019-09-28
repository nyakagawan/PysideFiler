from PySide2.QtWidgets import QDialog, QVBoxLayout, QWidget, QSplitter, QSizePolicy, QLayout, QTextBrowser
from multi_tab_pane import MultiTabPane
import PySide2.QtCore

class Filer(QDialog):

    def __init__(self, parent=None) -> None:
        super(Filer, self).__init__(parent)
        self.setup_ui()
        self.setWindowTitle("Filer")
        self._left_tab_pane = self.setting_up_tabs(self.vertical_layout_left)
        self._right_tab_pane = self.setting_up_tabs(self.vertical_layout_right)

    def setup_ui(self):
        vertical_layout = QVBoxLayout(self)
        vertical_layout.setSpacing(6)
        vertical_layout.setContentsMargins(11, 11, 11, 11)
        splitter_v = QSplitter(self);
        splitter_v.setOrientation(PySide2.QtCore.Qt.Vertical)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(splitter_v.sizePolicy().hasHeightForWidth())
        splitter_v.setSizePolicy(size_policy)
        splitter_h = QSplitter(splitter_v)
        splitter_h.setOrientation(PySide2.QtCore.Qt.Horizontal)
        vertical_layout_widget = QWidget(splitter_h)
        self.vertical_layout_left = QVBoxLayout(vertical_layout_widget)
        self.vertical_layout_left.setSpacing(6)
        self.vertical_layout_left.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.vertical_layout_left.setContentsMargins(0, 0, 0, 0)
        splitter_h.addWidget(vertical_layout_widget)
        vertical_layout_widget2 = QWidget(splitter_h)
        self.vertical_layout_right = QVBoxLayout(vertical_layout_widget2)
        self.vertical_layout_right.setContentsMargins(0, 0, 0, 0)
        splitter_h.addWidget(vertical_layout_widget2)
        splitter_v.addWidget(splitter_h)
        vertical_layout_widget3 = QWidget(splitter_v)
        vertical_layout_bottom = QVBoxLayout(vertical_layout_widget3)
        vertical_layout_bottom.setSpacing(6)
        vertical_layout_bottom.setSizeConstraint(QLayout.SetDefaultConstraint)
        vertical_layout_bottom.setContentsMargins(11, 0, 11, 11)
        text_browser = QTextBrowser(vertical_layout_widget3)
        vertical_layout_bottom.addWidget(text_browser)
        splitter_v.addWidget(vertical_layout_widget3)
        vertical_layout.addWidget(splitter_v)

    def setting_up_tabs(self, layout: QVBoxLayout) -> MultiTabPane:
        multi_tab_pane = MultiTabPane(self)
        layout.addWidget(multi_tab_pane)
        multi_tab_pane.add_tab("C:/")
        multi_tab_pane.set_current_tab_index(0)
        return multi_tab_pane
