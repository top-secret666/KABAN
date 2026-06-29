"""Настройка и обновление таблиц при смене темы."""

from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt

from ui.resources.theme_manager import current_palette


def configure_table(table: QTableWidget):
    """Единый современный вид таблиц."""
    table.setObjectName('data_table')
    table.setShowGrid(False)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setFocusPolicy(Qt.StrongFocus)
    table.verticalHeader().setVisible(False)
    table.verticalHeader().setDefaultSectionSize(44)
    table.horizontalHeader().setHighlightSections(False)
    table.horizontalHeader().setStretchLastSection(True)
    table.setWordWrap(False)


def _text_color():
    return QColor(current_palette()['text_primary'])


def style_item(item, bg=None):
    """Задаёт цвет текста и опционально фон ячейки."""
    if item is None:
        return
    item.setForeground(QBrush(_text_color()))
    if bg is not None:
        item.setBackground(QColor(bg))


def task_status_backgrounds():
    p = current_palette()
    return {
        'новая': p['status_new_bg'],
        'в работе': p['status_progress_bg'],
        'на проверке': p['status_review_bg'],
        'завершено': p['status_done_bg'],
    }


def apply_task_row_colors(table: QTableWidget, status_col=4, num_cols=7):
    """Подсветка строк задач по статусу (тема-зависимые цвета)."""
    colors = task_status_backgrounds()
    fg = _text_color()
    for row in range(table.rowCount()):
        status_item = table.item(row, status_col)
        status = status_item.text() if status_item else ''
        bg = colors.get(status)
        for col in range(num_cols):
            item = table.item(row, col)
            if item:
                item.setForeground(QBrush(fg))
                if bg:
                    item.setBackground(QColor(bg))


def refresh_table_theme(table: QTableWidget, status_col=None, num_cols=None):
    """Сбрасывает цвет текста ячеек после смены темы."""
    if table is None:
        return
    fg = _text_color()
    cols = num_cols or table.columnCount()
    for row in range(table.rowCount()):
        for col in range(cols):
            item = table.item(row, col)
            if item:
                item.setForeground(QBrush(fg))
    if status_col is not None and num_cols is not None:
        apply_task_row_colors(table, status_col, num_cols)


def refresh_all_tables(root):
    """Обновляет все таблицы в дереве виджетов."""
    for table in root.findChildren(QTableWidget):
        name = table.objectName()
        if table.property('task_status_col') is not None:
            refresh_table_theme(
                table,
                status_col=table.property('task_status_col'),
                num_cols=table.property('task_num_cols'),
            )
        else:
            refresh_table_theme(table)
