from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ui.resources.styles import TEXT_PRIMARY, TEXT_SECONDARY, BG_CARD, BORDER


class PageHeader(QFrame):
    """Верхняя полоса страницы в стиле Bitrix24."""

    def __init__(self, title, subtitle='', parent=None):
        super().__init__(parent)
        self.setObjectName('page_header')
        self.setFixedHeight(64 if not subtitle else 72)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 24, 0)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setObjectName('page_title')
        title_lbl.setFont(QFont('Segoe UI', 18, QFont.DemiBold))
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
    """Панель фильтров в белой карточке."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('filter_panel')
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(16, 12, 16, 12)
        self._layout.setSpacing(12)

    def add_widget(self, widget):
        self._layout.addWidget(widget)

    def add_stretch(self):
        self._layout.addStretch()

    def layout(self):
        return self._layout
