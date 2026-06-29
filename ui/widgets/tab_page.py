from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt

from ui.widgets.page_header import PageHeader


class TabPage(QWidget):
    """Обёртка вкладки: заголовок + контентная область в стиле Bitrix24."""

    def __init__(self, title, subtitle='', scrollable=False, parent=None):
        super().__init__(parent)
        self.setObjectName('page_content')

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.header = PageHeader(title, subtitle)
        root.addWidget(self.header)

        if scrollable:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.NoFrame)
            scroll.setStyleSheet('QScrollArea { background: transparent; border: none; }')
            self.body = QWidget()
            self.body.setStyleSheet('background: transparent;')
            self.content_layout = QVBoxLayout(self.body)
            scroll.setWidget(self.body)
            root.addWidget(scroll, stretch=1)
        else:
            self.body = QWidget()
            self.body.setObjectName('page_body')
            self.content_layout = QVBoxLayout(self.body)
            root.addWidget(self.body, stretch=1)

        self.content_layout.setContentsMargins(24, 20, 24, 20)
        self.content_layout.setSpacing(16)

    def add_action(self, widget):
        self.header.add_action(widget)
