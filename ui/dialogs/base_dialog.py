"""Базовый диалог с шапкой и корректными флагами окна."""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFrame, QWidget,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from ui.resources.theme_manager import get_stylesheet


def dialog_parent(widget):
    if widget is None:
        return None
    window = widget.window()
    return window if window else widget


class BaseDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super().__init__(dialog_parent(parent))
        if title:
            self.setWindowTitle(title)
        self._dialog_title = title
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumWidth(500)
        self._build_chrome(title)
        self._apply_style()
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 55))
        self.setGraphicsEffect(shadow)

    def _apply_style(self):
        self.setStyleSheet(get_stylesheet())

    def _build_chrome(self, title):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        accent = QFrame()
        accent.setObjectName('dialog_accent')
        accent.setFixedHeight(3)
        outer.addWidget(accent)

        self.body = QWidget()
        self.body.setObjectName('dialog_body')
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(24, 20, 24, 16)
        self.body_layout.setSpacing(14)
        outer.addWidget(self.body)

        self.footer = QFrame()
        self.footer.setObjectName('dialog_footer')
        self.footer.setFixedHeight(60)
        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(24, 10, 24, 14)
        self.footer_layout.addStretch()
        outer.addWidget(self.footer)

    def add_footer_button(self, widget):
        self.footer_layout.addWidget(widget)

    def showEvent(self, event):
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
