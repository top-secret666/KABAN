"""Генерация QSS по палитре цветов."""

FONT_FAMILY = "'Segoe UI', 'Open Sans', sans-serif"


def build_stylesheet(p):
    """Собирает полный stylesheet из словаря палитры."""
    return (
        _main_window(p) + _sidebar(p) + _page(p) + _form(p)
        + _buttons(p) + _tables(p) + _tabs(p) + _dialogs(p)
        + _notifications(p) + _kanban(p)
    )


def _main_window(p):
    return f"""
QMainWindow {{ background-color: {p['bg_main']}; }}
QMenuBar {{
    background-color: {p['bg_header']}; color: {p['text_primary']};
    border-bottom: 1px solid {p['border']}; padding: 2px 0;
    font-size: 13px; font-family: {FONT_FAMILY};
}}
QMenuBar::item {{ background: transparent; padding: 8px 14px; border-radius: 4px; margin: 2px 1px; }}
QMenuBar::item:selected {{ background-color: {p['primary_light']}; color: {p['primary_dark']}; }}
QMenu {{
    background-color: {p['bg_card']}; border: 1px solid {p['border']};
    border-radius: 6px; padding: 4px 0;
}}
QMenu::item {{ padding: 8px 28px 8px 16px; font-size: 13px; color: {p['text_primary']}; }}
QMenu::item:selected {{ background-color: {p['primary_light']}; color: {p['primary_dark']}; }}
QMenu::separator {{ height: 1px; background: {p['divider']}; margin: 4px 12px; }}
QStatusBar {{
    background-color: {p['bg_header']}; color: {p['text_secondary']};
    border-top: 1px solid {p['border']}; font-size: 12px; padding: 2px 12px;
}}
QStatusBar QLabel {{ color: {p['text_secondary']}; font-size: 12px; padding: 0 8px; }}
QToolBar {{
    background-color: {p['bg_header']}; border-bottom: 1px solid {p['border']};
    padding: 4px 12px; spacing: 4px;
}}
QToolBar QToolButton {{
    background: transparent; border: none; border-radius: 4px;
    padding: 6px 10px; font-size: 13px; color: {p['text_primary']};
}}
QToolBar QToolButton:hover {{ background-color: {p['primary_light']}; color: {p['primary_dark']}; }}
QScrollBar:vertical {{ border: none; background: transparent; width: 6px; }}
QScrollBar::handle:vertical {{ background: {p['scrollbar']}; border-radius: 3px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background: {p['scrollbar_hover']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ border: none; background: transparent; height: 6px; }}
QScrollBar::handle:horizontal {{ background: {p['scrollbar']}; border-radius: 3px; min-width: 30px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""


def _sidebar(p):
    return f"""
QFrame#sidebar {{
    background-color: {p['sidebar_bg']}; border: none;
    border-right: 1px solid {p['sidebar_border']};
}}
QFrame#sidebar_logo {{
    background-color: {p['sidebar_bg']}; border-bottom: 1px solid {p['sidebar_border']};
}}
QFrame#sidebar_user {{
    background-color: {p['sidebar_user_bg']}; border-top: 1px solid {p['sidebar_border']};
}}
QPushButton#sidebar_btn {{
    background: transparent; color: {p['sidebar_text_dim']}; border: none;
    border-radius: 6px; text-align: left; padding: 0 12px;
    font-family: {FONT_FAMILY}; font-size: 13px; font-weight: 500;
}}
QPushButton#sidebar_btn:hover {{ background-color: {p['sidebar_hover']}; color: {p['sidebar_text']}; }}
QPushButton#sidebar_btn:checked {{
    background-color: {p['sidebar_active_bg']}; color: {p['sidebar_text']};
    border-left: 3px solid {p['primary']}; padding-left: 9px;
}}
"""


def _page(p):
    return f"""
QFrame#page_header {{
    background-color: {p['bg_card']};
    border-bottom: 1px solid {p['border']};
}}
QLabel#page_title {{
    color: {p['text_primary']}; background: transparent; border: none;
    font-size: 18px; font-weight: 600;
}}
QLabel#page_subtitle {{
    color: {p['text_secondary']}; background: transparent; border: none;
    font-size: 11px;
}}
QFrame#filter_panel {{
    background-color: {p['bg_card']};
    border: 1px solid {p['border']};
    border-radius: 10px;
}}
QFrame#filter_panel QLabel {{
    color: {p['text_secondary']};
    font-size: 12px;
    font-weight: 500;
}}
QWidget#page_content, QWidget#page_body {{
    background-color: {p['bg_main']};
}}
QScrollArea {{
    background: transparent;
    border: none;
}}
"""


def _form(p):
    return f"""
QLabel {{ color: {p['text_primary']}; font-size: 13px; font-family: {FONT_FAMILY}; }}
QLineEdit, QTextEdit, QPlainTextEdit {{
    border: 1px solid {p['border']}; border-radius: 6px; padding: 8px 12px;
    background-color: {p['input_bg']}; color: {p['text_primary']};
    font-size: 14px; font-family: {FONT_FAMILY};
    selection-background-color: {p['primary_light']}; selection-color: {p['primary_dark']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{ border: 1px solid {p['primary']}; }}
QLineEdit:hover, QTextEdit:hover {{ border: 1px solid {p['border_hover']}; }}
QComboBox {{
    border: 1px solid {p['border']}; border-radius: 6px; padding: 7px 12px;
    background-color: {p['input_bg']}; color: {p['text_primary']}; font-size: 14px;
}}
QComboBox:hover {{ border: 1px solid {p['border_hover']}; }}
QComboBox:focus {{ border: 1px solid {p['primary']}; }}
QComboBox::drop-down {{ border: none; width: 24px; }}
QComboBox QAbstractItemView {{
    border: 1px solid {p['border']}; border-radius: 6px;
    background-color: {p['bg_card']}; selection-background-color: {p['primary_light']};
    color: {p['text_primary']};
}}
QDateEdit, QSpinBox, QDoubleSpinBox {{
    border: 1px solid {p['border']}; border-radius: 6px; padding: 7px 12px;
    background-color: {p['input_bg']}; color: {p['text_primary']}; font-size: 14px;
}}
QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{ border: 1px solid {p['primary']}; }}
QGroupBox {{
    font-weight: 600; font-size: 14px; color: {p['text_primary']};
    border: 1px solid {p['border']}; border-radius: 8px;
    margin-top: 14px; padding: 18px 12px 12px; background-color: {p['bg_card']};
}}
QGroupBox::title {{
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 14px; padding: 0 8px; background-color: {p['bg_card']};
}}
QCheckBox {{ font-size: 13px; color: {p['text_primary']}; spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px; border: 2px solid {p['border']};
    border-radius: 3px; background-color: {p['input_bg']};
}}
QCheckBox::indicator:checked {{ background-color: {p['primary']}; border-color: {p['primary']}; }}
QTextBrowser {{
    border: 1px solid {p['border']}; border-radius: 8px;
    background-color: {p['bg_card']}; color: {p['text_primary']};
    padding: 12px; font-size: 13px;
}}
"""


def _buttons(p):
    return f"""
QPushButton {{
    background-color: {p['primary']}; color: {p['text_on_primary']};
    border: none; border-radius: 8px; padding: 9px 22px;
    font-size: 13px; font-weight: 600; font-family: {FONT_FAMILY}; min-height: 18px;
}}
QPushButton:hover {{ background-color: {p['primary_dark']}; }}
QPushButton:pressed {{ background-color: {p['primary_pressed']}; }}
QPushButton:disabled {{ background-color: {p['border']}; color: {p['text_secondary']}; }}
QPushButton#primary {{
    background-color: {p['primary']}; color: {p['text_on_primary']};
    padding: 9px 20px; border-radius: 8px; font-weight: 600;
}}
QPushButton#primary:hover {{ background-color: {p['primary_dark']}; }}
QPushButton#success {{ background-color: {p['success']}; color: {p['text_primary']}; }}
QPushButton#warning {{ background-color: {p['warning']}; color: {p['text_primary']}; }}
QPushButton#error {{ background-color: {p['error']}; color: white; }}
QPushButton#flat {{
    background: transparent; color: {p['primary']};
    border: 1px solid {p['primary']}; font-weight: 500;
}}
QPushButton#flat:hover {{ background-color: {p['primary_light']}; }}
QPushButton#ghost {{
    background: transparent; color: {p['text_secondary']}; border: none; font-weight: 500;
}}
QPushButton#ghost:hover {{ color: {p['primary']}; background-color: {p['primary_light']}; }}
QPushButton#kanban_add {{
    background: transparent; color: {p['text_secondary']};
    border: 2px dashed {p['border']}; border-radius: 8px; padding: 12px;
}}
QPushButton#kanban_add:hover {{
    border-color: {p['primary']}; color: {p['primary']}; background-color: {p['primary_light']};
}}
"""


def _tables(p):
    return f"""
QTableWidget, QTableView, QTreeView {{
    border: 1px solid {p['border']};
    border-radius: 10px;
    background-color: {p['bg_card']};
    alternate-background-color: {p['table_alt']};
    selection-background-color: {p['primary']};
    selection-color: {p['text_on_primary']};
    gridline-color: transparent;
    font-size: 13px;
    color: {p['text_primary']};
    outline: none;
}}
QTableWidget#data_table, QTableView#data_table {{
    border: 1px solid {p['border']};
    background-color: {p['bg_card']};
}}
QTableWidget::item, QTableView::item {{
    padding: 10px 14px;
    color: {p['text_primary']};
    border: none;
    border-bottom: 1px solid {p['border_light']};
}}
QTableWidget::item:alternate, QTableView::item:alternate {{
    background-color: {p['table_alt']};
    color: {p['text_primary']};
}}
QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {p['primary']};
    color: {p['text_on_primary']};
}}
QTableWidget::item:hover, QTableView::item:hover {{
    background-color: {p['primary_light']};
    color: {p['text_primary']};
}}
QHeaderView::section {{
    background-color: {p['table_header']};
    padding: 12px 14px;
    border: none;
    border-bottom: 2px solid {p['border']};
    border-right: 1px solid {p['border_light']};
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    color: {p['text_secondary']};
}}
QHeaderView::section:last {{
    border-right: none;
}}
QTableCornerButton::section {{
    background-color: {p['table_header']};
    border: none;
}}
"""


def _tabs(p):
    return f"""
QTabWidget::pane {{
    border: 1px solid {p['border']}; border-radius: 0 0 8px 8px;
    background-color: {p['bg_card']}; top: -1px;
}}
QTabBar {{ background-color: {p['bg_card']}; border-bottom: 1px solid {p['border']}; }}
QTabBar::tab {{
    background: transparent; border: none; border-bottom: 2px solid transparent;
    padding: 10px 20px; font-size: 13px; font-weight: 500;
    color: {p['text_secondary']}; font-family: {FONT_FAMILY};
}}
QTabBar::tab:selected {{ color: {p['primary']}; border-bottom: 2px solid {p['primary']}; font-weight: 600; }}
QTabBar::tab:hover:!selected {{ color: {p['text_primary']}; background-color: {p['primary_light']}; }}
"""


def _dialogs(p):
    return f"""
QDialog {{
    background-color: {p['bg_card']}; border: 1px solid {p['border']}; border-radius: 10px;
}}
QFrame#dialog_accent {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {p['primary']}, stop:1 {p['primary_dark']});
    border: none;
    border-top-left-radius: 9px;
    border-top-right-radius: 9px;
    max-height: 3px;
    min-height: 3px;
}}
QWidget#dialog_body {{ background-color: {p['bg_card']}; border: none; }}
QFrame#dialog_footer {{
    background-color: {p['bg_card']}; border-top: 1px solid {p['border']};
    border-bottom-left-radius: 9px; border-bottom-right-radius: 9px;
}}
QMessageBox {{ background-color: {p['bg_card']}; }}
QMessageBox QLabel {{ color: {p['text_primary']}; font-size: 14px; }}
"""


def _notifications(p):
    return f"""
QFrame#notification_info {{ background-color: {p['status_new_bg']}; border-left: 4px solid {p['status_new']}; border-radius: 6px; }}
QFrame#notification_success {{ background-color: {p['status_done_bg']}; border-left: 4px solid {p['status_done']}; border-radius: 6px; }}
QFrame#notification_warning {{ background-color: {p['status_progress_bg']}; border-left: 4px solid {p['status_progress']}; border-radius: 6px; }}
QFrame#notification_error {{ background-color: {p['accent_light']}; border-left: 4px solid {p['error']}; border-radius: 6px; }}
QLabel#notification_text {{ color: {p['text_primary']}; font-weight: bold; }}
QPushButton#notification_close {{ background: transparent; color: {p['text_secondary']}; border: none; font-size: 16px; }}
QFrame#notifications_panel {{
    background-color: {p['bg_card']}; border: 1px solid {p['border']}; border-radius: 10px;
}}
"""


def _kanban(p):
    return f"""
QFrame#kanban_column {{ background-color: {p['kanban_col_bg']}; border-radius: 10px; }}
QFrame#kanban_column_new {{ background-color: {p['status_new_bg']}; border-radius: 10px; }}
QFrame#kanban_column_progress {{ background-color: {p['status_progress_bg']}; border-radius: 10px; }}
QFrame#kanban_column_review {{ background-color: {p['status_review_bg']}; border-radius: 10px; }}
QFrame#kanban_column_done {{ background-color: {p['status_done_bg']}; border-radius: 10px; }}
QFrame#kanban_card {{
    background-color: {p['bg_card']}; border-radius: 8px; border: 1px solid {p['border_light']};
}}
QFrame#kanban_card:hover {{ border: 1px solid {p['primary']}; }}
QLabel#kanban_col_title {{ font-size: 14px; font-weight: 700; color: {p['text_primary']}; }}
QLabel#card_title {{ font-size: 14px; font-weight: 600; color: {p['text_primary']}; }}
QLabel#card_project {{ font-size: 12px; color: {p['primary']}; font-weight: 500; }}
QLabel#card_developer, QLabel#card_hours {{ font-size: 12px; color: {p['text_secondary']}; }}
QFrame#stat_card {{
    background-color: {p['bg_card']}; border-radius: 10px; border: 1px solid {p['border_light']};
}}
QFrame#stat_card:hover {{ border: 1px solid {p['primary']}; }}
QLabel#stat_value {{ font-size: 28px; font-weight: 700; color: {p['text_primary']}; }}
QLabel#stat_title {{ font-size: 13px; color: {p['text_secondary']}; }}
"""
