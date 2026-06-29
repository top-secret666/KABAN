"""
KABAN:manager — тема в стиле Bitrix24
"""

# ═══════════════════════════════════════════════════════
# ЦВЕТОВАЯ ПАЛИТРА BITRIX24
# ═══════════════════════════════════════════════════════

PRIMARY_COLOR = "#2FC6F6"
PRIMARY_DARK = "#1BA8D4"
PRIMARY_LIGHT = "#E8F9FE"
SECONDARY_COLOR = "#525C69"
SUCCESS_COLOR = "#9DCF00"
WARNING_COLOR = "#FFA900"
ERROR_COLOR = "#FF5752"
INFO_COLOR = "#2FC6F6"
LIGHT_COLOR = "#F5F7F8"
DARK_COLOR = "#333B4F"

ACCENT = "#FF5752"
ACCENT_LIGHT = "#FFF0F0"

BG_MAIN = "#EDEEF0"
BG_CARD = "#FFFFFF"
BG_HEADER = "#FFFFFF"

TEXT_PRIMARY = "#333333"
TEXT_SECONDARY = "#828B95"
TEXT_WHITE = "#FFFFFF"

BORDER = "#E0E4EA"
BORDER_LIGHT = "#EEF0F3"
DIVIDER = "#E8EAED"

# Боковая панель
SIDEBAR_BG = "#333B4F"
SIDEBAR_HOVER = "#3E4659"
SIDEBAR_ACTIVE = "#2FC6F6"
SIDEBAR_TEXT = "#FFFFFF"
SIDEBAR_TEXT_DIM = "#A8B0BC"
SIDEBAR_BORDER = "#2A3140"

# Статусы Kanban
STATUS_NEW = "#2FC6F6"
STATUS_NEW_BG = "#E8F9FE"
STATUS_PROGRESS = "#FFA900"
STATUS_PROGRESS_BG = "#FFF8E6"
STATUS_REVIEW = "#9B59B6"
STATUS_REVIEW_BG = "#F5EEFF"
STATUS_DONE = "#9DCF00"
STATUS_DONE_BG = "#F3FBE6"

FONT_FAMILY = "'Segoe UI', 'Open Sans', sans-serif"

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
    font-family: {FONT_FAMILY};
}}
QMenuBar::item {{
    background-color: transparent;
    padding: 8px 14px;
    border-radius: 4px;
    margin: 2px 1px;
}}
QMenuBar::item:selected {{
    background-color: {PRIMARY_LIGHT};
    color: {PRIMARY_DARK};
}}
QMenu {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 4px 0;
}}
QMenu::item {{
    padding: 8px 28px 8px 16px;
    font-size: 13px;
}}
QMenu::item:selected {{
    background-color: {PRIMARY_LIGHT};
    color: {PRIMARY_DARK};
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
    padding: 2px 12px;
}}
QStatusBar QLabel {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    padding: 0 8px;
}}

QToolBar {{
    background-color: {BG_HEADER};
    border-bottom: 1px solid {BORDER};
    padding: 4px 12px;
    spacing: 4px;
}}
QToolBar QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 13px;
    color: {TEXT_PRIMARY};
}}
QToolBar QToolButton:hover {{
    background-color: {PRIMARY_LIGHT};
    color: {PRIMARY_DARK};
}}

QScrollBar:vertical {{
    border: none;
    background: transparent;
    width: 6px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: #C5CAD3;
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: #A0A8B4;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    border: none;
    background: transparent;
    height: 6px;
}}
QScrollBar::handle:horizontal {{
    background: #C5CAD3;
    border-radius: 3px;
    min-width: 30px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
"""

# ═══════════════════════════════════════════════════════
# БОКОВАЯ ПАНЕЛЬ
# ═══════════════════════════════════════════════════════

SIDEBAR_STYLE = f"""
QFrame#sidebar {{
    background-color: {SIDEBAR_BG};
    border: none;
    border-right: 1px solid {SIDEBAR_BORDER};
}}
QFrame#sidebar_logo {{
    background-color: {SIDEBAR_BG};
    border-bottom: 1px solid {SIDEBAR_BORDER};
}}
QFrame#sidebar_nav {{
    background-color: transparent;
    border: none;
}}
QFrame#sidebar_user {{
    background-color: #2A3140;
    border-top: 1px solid {SIDEBAR_BORDER};
}}
QLabel#sidebar_avatar {{
    background-color: {SIDEBAR_HOVER};
    border-radius: 18px;
    color: {TEXT_WHITE};
}}

QPushButton#sidebar_btn {{
    background-color: transparent;
    color: {SIDEBAR_TEXT_DIM};
    border: none;
    border-radius: 6px;
    text-align: left;
    padding: 0 12px;
    font-family: {FONT_FAMILY};
    font-size: 13px;
    font-weight: 500;
}}
QPushButton#sidebar_btn:hover {{
    background-color: {SIDEBAR_HOVER};
    color: {SIDEBAR_TEXT};
}}
QPushButton#sidebar_btn:checked {{
    background-color: rgba(47, 198, 246, 0.15);
    color: {SIDEBAR_TEXT};
    border-left: 3px solid {SIDEBAR_ACTIVE};
    padding-left: 9px;
}}
"""

# ═══════════════════════════════════════════════════════
# СТРАНИЦЫ И КОНТЕНТ
# ═══════════════════════════════════════════════════════

PAGE_STYLE = f"""
QFrame#page_header {{
    background-color: {BG_CARD};
    border-bottom: 1px solid {BORDER};
}}
QLabel#page_title {{
    color: {TEXT_PRIMARY};
    background: transparent;
    border: none;
}}
QLabel#page_subtitle {{
    color: {TEXT_SECONDARY};
    background: transparent;
    border: none;
}}

QFrame#filter_panel {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}
QFrame#content_card {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

QWidget#page_content {{
    background-color: {BG_MAIN};
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ ФОРМ
# ═══════════════════════════════════════════════════════

FORM_STYLE = f"""
QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-family: {FONT_FAMILY};
}}

QLineEdit, QTextEdit, QPlainTextEdit {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 8px 12px;
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    font-size: 14px;
    font-family: {FONT_FAMILY};
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {PRIMARY_DARK};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1px solid {PRIMARY_COLOR};
}}
QLineEdit:hover, QTextEdit:hover {{
    border: 1px solid #C0C8D6;
}}

QComboBox {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 7px 12px;
    background-color: {BG_CARD};
    color: {TEXT_PRIMARY};
    font-size: 14px;
    min-height: 20px;
}}
QComboBox:hover {{
    border: 1px solid #C0C8D6;
}}
QComboBox:focus {{
    border: 1px solid {PRIMARY_COLOR};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    background-color: {BG_CARD};
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {PRIMARY_DARK};
    padding: 4px;
    outline: none;
}}

QDateEdit {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 7px 12px;
    background-color: {BG_CARD};
    font-size: 14px;
}}
QDateEdit:focus {{
    border: 1px solid {PRIMARY_COLOR};
}}
QDateEdit::drop-down {{
    border: none;
    width: 24px;
}}

QSpinBox, QDoubleSpinBox {{
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 7px 12px;
    background-color: {BG_CARD};
    font-size: 14px;
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1px solid {PRIMARY_COLOR};
}}

QGroupBox {{
    font-weight: 600;
    font-size: 14px;
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 8px;
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
    border-radius: 3px;
    background-color: {BG_CARD};
}}
QCheckBox::indicator:checked {{
    background-color: {PRIMARY_COLOR};
    border-color: {PRIMARY_COLOR};
}}

QTextBrowser {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    background-color: {BG_CARD};
    padding: 12px;
    font-size: 13px;
    font-family: {FONT_FAMILY};
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
    border-radius: 4px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    font-family: {FONT_FAMILY};
    min-height: 16px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_DARK};
}}
QPushButton:pressed {{
    background-color: #1596BE;
}}
QPushButton:disabled {{
    background-color: #DCE0E8;
    color: #A0A8B8;
}}

QPushButton#success {{
    background-color: {SUCCESS_COLOR};
    color: {TEXT_PRIMARY};
}}
QPushButton#success:hover {{
    background-color: #8AB800;
}}
QPushButton#warning {{
    background-color: {WARNING_COLOR};
    color: {TEXT_PRIMARY};
}}
QPushButton#warning:hover {{
    background-color: #E69800;
}}
QPushButton#error {{
    background-color: {ERROR_COLOR};
}}
QPushButton#error:hover {{
    background-color: #E04440;
}}

QPushButton#flat {{
    background-color: transparent;
    color: {PRIMARY_DARK};
    border: 1px solid {PRIMARY_COLOR};
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
    color: {PRIMARY_DARK};
    background-color: {PRIMARY_LIGHT};
}}

QPushButton#kanban_add {{
    background-color: transparent;
    color: {TEXT_SECONDARY};
    border: 2px dashed {BORDER};
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    padding: 12px;
}}
QPushButton#kanban_add:hover {{
    border-color: {PRIMARY_COLOR};
    color: {PRIMARY_DARK};
    background-color: {PRIMARY_LIGHT};
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ ТАБЛИЦ
# ═══════════════════════════════════════════════════════

TABLE_STYLE = f"""
QTableWidget, QTableView, QTreeView {{
    border: 1px solid {BORDER};
    border-radius: 8px;
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
    font-family: {FONT_FAMILY};
}}
"""

# ═══════════════════════════════════════════════════════
# ВКЛАДКИ (внутренние, напр. в отчётах)
# ═══════════════════════════════════════════════════════

TAB_STYLE = f"""
QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 0 0 8px 8px;
    background-color: {BG_CARD};
    top: -1px;
}}
QTabBar {{
    background-color: {BG_CARD};
    border-bottom: 1px solid {BORDER};
}}
QTabBar::tab {{
    background-color: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 500;
    color: {TEXT_SECONDARY};
    font-family: {FONT_FAMILY};
}}
QTabBar::tab:selected {{
    color: {PRIMARY_DARK};
    border-bottom: 2px solid {PRIMARY_COLOR};
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    color: {TEXT_PRIMARY};
    background-color: {PRIMARY_LIGHT};
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

QProgressBar {{
    border: none;
    border-radius: 3px;
    background-color: rgba(255,255,255,0.2);
    height: 4px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {PRIMARY_COLOR};
    border-radius: 3px;
}}
"""

# ═══════════════════════════════════════════════════════
# СТИЛИ УВЕДОМЛЕНИЙ
# ═══════════════════════════════════════════════════════

NOTIFICATION_STYLE = f"""
QFrame#notification_info {{
    background-color: {STATUS_NEW_BG};
    border-left: 4px solid {STATUS_NEW};
    border-radius: 6px;
    padding: 4px;
}}
QFrame#notification_success {{
    background-color: {STATUS_DONE_BG};
    border-left: 4px solid {STATUS_DONE};
    border-radius: 6px;
    padding: 4px;
}}
QFrame#notification_warning {{
    background-color: {STATUS_PROGRESS_BG};
    border-left: 4px solid {STATUS_PROGRESS};
    border-radius: 6px;
    padding: 4px;
}}
QFrame#notification_error {{
    background-color: {ACCENT_LIGHT};
    border-left: 4px solid {ACCENT};
    border-radius: 6px;
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
    border-radius: 10px;
    border: none;
}}
QFrame#kanban_column_new {{
    background-color: {STATUS_NEW_BG};
    border-radius: 10px;
    border: none;
}}
QFrame#kanban_column_progress {{
    background-color: {STATUS_PROGRESS_BG};
    border-radius: 10px;
    border: none;
}}
QFrame#kanban_column_review {{
    background-color: {STATUS_REVIEW_BG};
    border-radius: 10px;
    border: none;
}}
QFrame#kanban_column_done {{
    background-color: {STATUS_DONE_BG};
    border-radius: 10px;
    border: none;
}}

QFrame#kanban_card {{
    background-color: {BG_CARD};
    border-radius: 8px;
    border: 1px solid {BORDER_LIGHT};
}}
QFrame#kanban_card:hover {{
    border: 1px solid {PRIMARY_COLOR};
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

QLabel#kanban_col_title {{
    font-size: 14px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    font-family: {FONT_FAMILY};
}}
QLabel#kanban_col_count_new {{
    background-color: {STATUS_NEW};
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}
QLabel#kanban_col_count_progress {{
    background-color: {STATUS_PROGRESS};
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}
QLabel#kanban_col_count_review {{
    background-color: {STATUS_REVIEW};
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_WHITE};
    border-radius: 10px;
    padding: 2px 8px;
}}
QLabel#kanban_col_count_done {{
    background-color: {STATUS_DONE};
    font-size: 11px;
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
    color: {PRIMARY_DARK};
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

QFrame#stat_card {{
    background-color: {BG_CARD};
    border-radius: 10px;
    border: 1px solid {BORDER_LIGHT};
}}
QFrame#stat_card:hover {{
    border: 1px solid {PRIMARY_COLOR};
}}
QLabel#stat_value {{
    font-size: 28px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    font-family: {FONT_FAMILY};
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

QFrame#notifications_panel {{
    background-color: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
"""

GLOBAL_STYLE = (
    MAIN_WINDOW_STYLE + SIDEBAR_STYLE + PAGE_STYLE + FORM_STYLE
    + BUTTON_STYLE + TABLE_STYLE + TAB_STYLE + DIALOG_STYLE
    + NOTIFICATION_STYLE + KANBAN_STYLE
)

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
