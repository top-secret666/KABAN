"""
KABAN:manager — Современная тема в стиле Bitrix24 Kanban
Профессиональный дизайн с Material Design элементами
"""

# ═══════════════════════════════════════════════════════
# ЦВЕТОВАЯ ПАЛИТРА
# ═══════════════════════════════════════════════════════

PRIMARY_COLOR = "#2B5CE6"
SECONDARY_COLOR = "#424242"
SUCCESS_COLOR = "#2FC6B0"
WARNING_COLOR = "#FFB800"
ERROR_COLOR = "#FF5752"
INFO_COLOR = "#00C4FB"
LIGHT_COLOR = "#F5F7FA"
DARK_COLOR = "#333B4F"

# Дополнительные цвета
PRIMARY_DARK = "#1E43B0"
PRIMARY_LIGHT = "#EBF0FF"
ACCENT = "#FF5752"
ACCENT_LIGHT = "#FFF0F0"

BG_MAIN = "#F5F7FA"
BG_CARD = "#FFFFFF"
BG_HEADER = "#FFFFFF"

TEXT_PRIMARY = "#333B4F"
TEXT_SECONDARY = "#8B95A5"
TEXT_WHITE = "#FFFFFF"

BORDER = "#E5E9F2"
BORDER_LIGHT = "#F0F2F5"
DIVIDER = "#ECEEF2"

# Статусы Kanban
STATUS_NEW = "#00C4FB"
STATUS_NEW_BG = "#E6F9FF"
STATUS_PROGRESS = "#FFB800"
STATUS_PROGRESS_BG = "#FFF8E6"
STATUS_REVIEW = "#9B59B6"
STATUS_REVIEW_BG = "#F5EEFF"
STATUS_DONE = "#2FC6B0"
STATUS_DONE_BG = "#E6FFF9"

# ═══════════════════════════════════════════════════════
# СТИЛИ ГЛАВНОГО ОКНА
# ═══════════════════════════════════════════════════════

MAIN_WINDOW_STYLE = f"""
QMainWindow {{
    background-color: {BG_MAIN};
}}

QMenuBar {{
    background-color: {BG_HEADER};
    color: {TEXT_PRIMARY};
    border-bottom: 1px solid {BORDER};
    padding: 2px 0;
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
}}
QMenuBar::item {{
    background-color: transparent;
    padding: 8px 14px;
    border-radius: 6px;
    margin: 2px 1px;
}}
QMenuBar::item:selected {{
    background-color: {PRIMARY_LIGHT};
    color: {PRIMARY_COLOR};
}}
QMenu {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 6px 0;
}}
QMenu::item {{
    padding: 8px 28px 8px 16px;
    font-size: 13px;
    border-radius: 4px;
    margin: 2px 6px;
}}
QMenu::item:selected {{
    background-color: {PRIMARY_LIGHT};
    color: {PRIMARY_COLOR};
}}
QMenu::separator {{
    height: 1px;
    background: {DIVIDER};
    margin: 4px 12px;
}}

QStatusBar {{
    background-color: {BG_HEADER};
    color: {TEXT_SECONDARY};
    border-top: 1px solid {BORDER};
    font-size: 12px;
    padding: 4px 12px;
}}

QTabWidget::pane {{
    border: none;
    background-color: {BG_MAIN};
}}
QTabBar {{
    background-color: {BG_HEADER};
    border-bottom: 1px solid {BORDER};
    qproperty-drawBase: 0;
}}
QTabBar::tab {{
    background-color: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    padding: 12px 22px;
    margin-right: 0;
    font-size: 14px;
    font-weight: 500;
    color: {TEXT_SECONDARY};
    font-family: 'Segoe UI', sans-serif;
}}
QTabBar::tab:selected {{
    color: {PRIMARY_COLOR};
    border-bottom: 3px solid {PRIMARY_COLOR};
    background-color: transparent;
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT_PRIMARY};
    border-bottom: 3px solid {BORDER};
}}

QToolBar {{
    background-color: {BG_HEADER};
    border-bottom: 1px solid {BORDER};
    padding: 4px 8px;
    spacing: 4px;
}}
QToolBar QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
    color: {TEXT_PRIMARY};
}}
QToolBar QToolButton:hover {{
    background-color: {PRIMARY_LIGHT};
    color: {PRIMARY_COLOR};
}}

QScrollBar:vertical {{
    border: none;
    background: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #C8CDD6;
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #A8B0BC;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    border: none;
    background: transparent;
    height: 8px;
    margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: #C8CDD6;
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background: #A8B0BC;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ ФОРМ
# ═══════════════════════════════════════════════════════

FORM_STYLE = f"""
QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
}}

QLineEdit, QTextEdit, QPlainTextEdit {{
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 10px 14px;
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    font-size: 14px;
    font-family: 'Segoe UI', sans-serif;
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {PRIMARY_COLOR};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1.5px solid {PRIMARY_COLOR};
}}
QLineEdit:hover, QTextEdit:hover {{
    border: 1.5px solid #C0C8D6;
}}

QComboBox {{
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 8px 14px;
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    font-size: 14px;
    min-height: 20px;
}}
QComboBox:hover {{
    border: 1.5px solid #C0C8D6;
}}
QComboBox:focus {{
    border: 1.5px solid {PRIMARY_COLOR};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox QAbstractItemView {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    background-color: {BG_CARD};
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {PRIMARY_COLOR};
    padding: 4px;
    outline: none;
}}

QDateEdit {{
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 8px 14px;
    background-color: {BG_CARD};
    font-size: 14px;
}}
QDateEdit:focus {{
    border: 1.5px solid {PRIMARY_COLOR};
}}
QDateEdit::drop-down {{
    border: none;
    width: 28px;
}}

QSpinBox, QDoubleSpinBox {{
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 8px 14px;
    background-color: {BG_CARD};
    font-size: 14px;
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1.5px solid {PRIMARY_COLOR};
}}

QGroupBox {{
    font-weight: 600;
    font-size: 14px;
    color: {TEXT_PRIMARY};
    border: 1.5px solid {BORDER};
    border-radius: 10px;
    margin-top: 14px;
    padding: 18px 12px 12px 12px;
    background-color: {BG_CARD};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 8px;
    background-color: {BG_CARD};
}}

QCheckBox {{
    font-size: 13px;
    color: {TEXT_PRIMARY};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {BORDER};
    border-radius: 4px;
    background-color: {BG_CARD};
}}
QCheckBox::indicator:checked {{
    background-color: {PRIMARY_COLOR};
    border-color: {PRIMARY_COLOR};
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ КНОПОК
# ═══════════════════════════════════════════════════════

BUTTON_STYLE = f"""
QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: {TEXT_WHITE};
    border: none;
    border-radius: 8px;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
    min-height: 16px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_DARK};
}}
QPushButton:pressed {{
    background-color: #1A3A9C;
}}
QPushButton:disabled {{
    background-color: #DCE0E8;
    color: #A0A8B8;
}}

QPushButton#success {{
    background-color: {SUCCESS_COLOR};
}}
QPushButton#success:hover {{
    background-color: #24A898;
}}
QPushButton#warning {{
    background-color: {WARNING_COLOR};
    color: {TEXT_PRIMARY};
}}
QPushButton#warning:hover {{
    background-color: #E6A600;
}}
QPushButton#error {{
    background-color: {ACCENT};
}}
QPushButton#error:hover {{
    background-color: #E04440;
}}

QPushButton#flat {{
    background-color: transparent;
    color: {PRIMARY_COLOR};
    border: 1.5px solid {PRIMARY_COLOR};
    font-weight: 500;
}}
QPushButton#flat:hover {{
    background-color: {PRIMARY_LIGHT};
}}

QPushButton#ghost {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    font-weight: 500;
}}
QPushButton#ghost:hover {{
    color: {PRIMARY_COLOR};
    background-color: {PRIMARY_LIGHT};
}}

QPushButton#kanban_add {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: 2px dashed {BORDER};
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
    padding: 12px;
}}
QPushButton#kanban_add:hover {{
    border-color: {PRIMARY_COLOR};
    color: {PRIMARY_COLOR};
    background-color: {PRIMARY_LIGHT};
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ ТАБЛИЦ
# ═══════════════════════════════════════════════════════

TABLE_STYLE = f"""
QTableWidget, QTableView, QTreeView {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    background-color: {BG_CARD};
    alternate-background-color: #FAFBFC;
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {TEXT_PRIMARY};
    gridline-color: {BORDER_LIGHT};
    font-size: 13px;
    outline: none;
}}
QTableWidget::item, QTableView::item {{
    padding: 8px 12px;
    border-bottom: 1px solid {BORDER_LIGHT};
}}
QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {PRIMARY_LIGHT};
    color: {TEXT_PRIMARY};
}}
QHeaderView::section {{
    background-color: #F7F8FA;
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid {BORDER};
    border-right: 1px solid {BORDER_LIGHT};
    font-weight: 600;
    font-size: 12px;
    color: {TEXT_SECONDARY};
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ ДИАЛОГОВ
# ═══════════════════════════════════════════════════════

DIALOG_STYLE = f"""
QDialog {{
    background-color: {BG_CARD};
}}
QDialog QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
}}
QDialog QPushButton {{
    min-width: 90px;
}}

QMessageBox {{
    background-color: {BG_CARD};
}}
QMessageBox QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 14px;
}}

QInputDialog {{
    background-color: {BG_CARD};
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ УВЕДОМЛЕНИЙ
# ═══════════════════════════════════════════════════════

NOTIFICATION_STYLE = f"""
QFrame#notification_info {{
    background-color: #E8F4FD;
    border-left: 4px solid {STATUS_NEW};
    border-radius: 8px;
    padding: 4px;
}}
QFrame#notification_success {{
    background-color: {STATUS_DONE_BG};
    border-left: 4px solid {STATUS_DONE};
    border-radius: 8px;
    padding: 4px;
}}
QFrame#notification_warning {{
    background-color: {STATUS_PROGRESS_BG};
    border-left: 4px solid {STATUS_PROGRESS};
    border-radius: 8px;
    padding: 4px;
}}
QFrame#notification_error {{
    background-color: {ACCENT_LIGHT};
    border-left: 4px solid {ACCENT};
    border-radius: 8px;
    padding: 4px;
}}

QLabel#notification_text {{
    color: {TEXT_PRIMARY};
    font-weight: bold;
}}

QPushButton#notification_close {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: none;
    font-weight: bold;
    font-size: 16px;
}}
"""

# ═══════════════════════════════════════════════════════
# KANBAN СТИЛИ
# ═══════════════════════════════════════════════════════

KANBAN_STYLE = f"""
QFrame#kanban_column {{
    background-color: #F0F2F5;
    border-radius: 12px;
    border: none;
}}
QFrame#kanban_column_new {{
    background-color: {STATUS_NEW_BG};
    border-radius: 12px;
    border: none;
}}
QFrame#kanban_column_progress {{
    background-color: {STATUS_PROGRESS_BG};
    border-radius: 12px;
    border: none;
}}
QFrame#kanban_column_review {{
    background-color: {STATUS_REVIEW_BG};
    border-radius: 12px;
    border: none;
}}
QFrame#kanban_column_done {{
    background-color: {STATUS_DONE_BG};
    border-radius: 12px;
    border: none;
}}

QFrame#kanban_card {{
    background-color: {BG_CARD};
    border-radius: 10px;
    border: 1px solid {BORDER_LIGHT};
}}
QFrame#kanban_card:hover {{
    border: 1px solid {PRIMARY_COLOR};
}}

QLabel#kanban_col_title {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', sans-serif;
}}
QLabel#kanban_col_count {{
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
    min-width: 20px;
}}
QLabel#kanban_col_count_new {{
    background-color: {STATUS_NEW};
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}
QLabel#kanban_col_count_progress {{
    background-color: {STATUS_PROGRESS};
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}
QLabel#kanban_col_count_review {{
    background-color: {STATUS_REVIEW};
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}
QLabel#kanban_col_count_done {{
    background-color: {STATUS_DONE};
    font-size: 12px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}

QLabel#card_title {{
    font-size: 14px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
}}
QLabel#card_project {{
    font-size: 12px;
    color: {PRIMARY_COLOR};
    font-weight: 500;
}}
QLabel#card_developer {{
    font-size: 12px;
    color: {TEXT_SECONDARY};
}}
QLabel#card_hours {{
    font-size: 11px;
    color: {TEXT_SECONDARY};
}}
QLabel#card_date {{
    font-size: 11px;
    color: #B0B8C8;
}}

QLabel#badge_new {{
    background-color: {STATUS_NEW};
    color: white;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}}
QLabel#badge_progress {{
    background-color: {STATUS_PROGRESS};
    color: white;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}}
QLabel#badge_review {{
    background-color: {STATUS_REVIEW};
    color: white;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}}
QLabel#badge_done {{
    background-color: {STATUS_DONE};
    color: white;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}}

QFrame#stat_card {{
    background-color: {BG_CARD};
    border-radius: 14px;
    border: 1px solid {BORDER_LIGHT};
}}
QFrame#stat_card:hover {{
    border: 1px solid {PRIMARY_COLOR};
}}
QLabel#stat_value {{
    font-size: 32px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', sans-serif;
}}
QLabel#stat_title {{
    font-size: 13px;
    font-weight: 500;
    color: {TEXT_SECONDARY};
}}
QLabel#stat_subtitle {{
    font-size: 11px;
    color: #B0B8C8;
}}
"""

# Объединение всех стилей
GLOBAL_STYLE = MAIN_WINDOW_STYLE + FORM_STYLE + BUTTON_STYLE + TABLE_STYLE + DIALOG_STYLE + NOTIFICATION_STYLE + KANBAN_STYLE

# Экспорт цветов для Python-кода
COLORS = {
    'primary': PRIMARY_COLOR,
    'primary_dark': PRIMARY_DARK,
    'primary_light': PRIMARY_LIGHT,
    'accent': ACCENT,
    'bg_main': BG_MAIN,
    'bg_card': BG_CARD,
    'text_primary': TEXT_PRIMARY,
    'text_secondary': TEXT_SECONDARY,
    'border': BORDER,
    'status_new': STATUS_NEW,
    'status_new_bg': STATUS_NEW_BG,
    'status_progress': STATUS_PROGRESS,
    'status_progress_bg': STATUS_PROGRESS_BG,
    'status_review': STATUS_REVIEW,
    'status_review_bg': STATUS_REVIEW_BG,
    'status_done': STATUS_DONE,
    'status_done_bg': STATUS_DONE_BG,
}
