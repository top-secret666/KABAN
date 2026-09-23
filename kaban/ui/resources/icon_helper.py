"""Вспомогательные иконки через стандартный набор Qt (без внешних файлов)."""

from PyQt5.QtWidgets import QApplication, QStyle
from PyQt5.QtGui import QIcon


def app_icon():
    icon = QIcon('ui/resources/icons/app_icon.png')
    return icon if not icon.isNull() else QIcon('ui/resources/icons/logo.png')


def std_icon(sp):
    return QApplication.style().standardIcon(sp)


ICONS = {
    'add': lambda: std_icon(QStyle.SP_FileDialogNewFolder),
    'edit': lambda: std_icon(QStyle.SP_FileDialogDetailedView),
    'delete': lambda: std_icon(QStyle.SP_TrashIcon),
    'refresh': lambda: std_icon(QStyle.SP_BrowserReload),
    'export': lambda: std_icon(QStyle.SP_DialogSaveButton),
    'save': lambda: std_icon(QStyle.SP_DialogSaveButton),
    'report': lambda: std_icon(QStyle.SP_FileDialogContentsView),
    'about': lambda: std_icon(QStyle.SP_MessageBoxInformation),
    'project': lambda: std_icon(QStyle.SP_DirIcon),
    'task': lambda: std_icon(QStyle.SP_FileIcon),
    'developer': lambda: std_icon(QStyle.SP_ComputerIcon),
    'info': lambda: std_icon(QStyle.SP_MessageBoxInformation),
    'success': lambda: std_icon(QStyle.SP_DialogApplyButton),
    'warning': lambda: std_icon(QStyle.SP_MessageBoxWarning),
    'error': lambda: std_icon(QStyle.SP_MessageBoxCritical),
    'backup': lambda: std_icon(QStyle.SP_DriveHDIcon),
}


def get_icon(name):
    factory = ICONS.get(name)
    if factory:
        return factory()
    return app_icon()
