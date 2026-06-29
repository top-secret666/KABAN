"""Базовый диалог с корректными флагами окна (исправляет «невидимые» диалоги)."""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from ui.resources.styles import DIALOG_STYLE, FORM_STYLE, BUTTON_STYLE


def dialog_parent(widget):
    """Возвращает главное окно как родителя для модального диалога."""
    if widget is None:
        return None
    window = widget.window()
    return window if window else widget


class BaseDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super().__init__(dialog_parent(parent))
        if title:
            self.setWindowTitle(title)
        self.setWindowFlags(
            Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint
        )
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumWidth(480)
        self.setStyleSheet(DIALOG_STYLE + FORM_STYLE + BUTTON_STYLE)

    def showEvent(self, event):
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
