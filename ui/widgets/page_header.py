from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont


class PageHeader(QFrame):

    def __init__(self, title, subtitle='', parent=None):
        super().__init__(parent)
        self.setObjectName('page_header')
        self.setFixedHeight(80 if not subtitle else 88)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(32, 16, 32, 16)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setObjectName('page_title')
        title_lbl.setFont(QFont('Segoe UI', 22, QFont.Bold))
        text_col.addWidget(title_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setObjectName('page_subtitle')
            sub_lbl.setFont(QFont('Segoe UI', 11))
            text_col.addWidget(sub_lbl)

        layout.addLayout(text_col)
        layout.addStretch()

        self._actions = QHBoxLayout()
        self._actions.setSpacing(8)
        layout.addLayout(self._actions)

    def add_action(self, widget):
        self._actions.addWidget(widget)


class FilterPanel(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('filter_panel')
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(20, 16, 20, 16)
        self._layout.setSpacing(12)

    def add_widget(self, widget):
        self._layout.addWidget(widget)

    def add_stretch(self):
        self._layout.addStretch()

    def layout(self):
        return self._layout
