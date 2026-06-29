"""Генерация QSS по палитре цветов."""

FONT_FAMILY = "'Segoe UI', 'Inter', system-ui, sans-serif"


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
    background-color: transparent; color: {p['text_secondary']};
    border: none; padding: 4px 8px;
    font-size: 12px; font-family: {FONT_FAMILY};
}}
QMenuBar::item {{ background: transparent; padding: 6px 12px; border-radius: 6px; }}
QMenuBar::item:selected {{ background-color: {p['primary_light']}; color: {p['primary_dark']}; }}
QMenu {{
    background-color: {p['bg_card']}; border: 1px solid {p['border']};
    border-radius: 10px; padding: 6px 0;
}}
QMenu::item {{ padding: 8px 28px 8px 16px; font-size: 13px; color: {p['text_primary']}; }}
QMenu::item:selected {{ background-color: {p['primary_light']}; color: {p['primary_dark']}; }}
QMenu::separator {{ height: 1px; background: {p['divider']}; margin: 4px 12px; }}
QStatusBar {{
    background-color: {p['bg_main']}; color: {p['text_secondary']};
    border-top: none; font-size: 11px; padding: 4px 16px;
}}
QStatusBar QLabel {{ color: {p['text_secondary']}; font-size: 11px; padding: 0 6px; }}
QToolBar {{ height: 0; max-height: 0; border: none; padding: 0; margin: 0; }}
QScrollBar:vertical {{ border: none; background: transparent; width: 8px; margin: 4px 2px; }}
QScrollBar::handle:vertical {{ background: {p['scrollbar']}; border-radius: 4px; min-height: 40px; }}
QScrollBar::handle:vertical:hover {{ background: {p['scrollbar_hover']}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ border: none; background: transparent; height: 8px; margin: 2px 4px; }}
QScrollBar::handle:horizontal {{ background: {p['scrollbar']}; border-radius: 4px; min-width: 40px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""


def _sidebar(p):
    return f"""
QFrame#sidebar {{
    background-color: {p['sidebar_bg']}; border: none;
    border-right: 1px solid {p['sidebar_border']};
}}
QFrame#sidebar_logo {{
    background-color: transparent; border: none;
}}
QFrame#sidebar_nav {{
    background-color: transparent; border: none;
}}
QFrame#sidebar_user {{
    background-color: {p['sidebar_user_bg']}; border-top: 1px solid {p['sidebar_border']};
}}
QLabel#sidebar_avatar {{
    background-color: {p['primary']}; border-radius: 18px;
    color: {p['text_on_primary']}; font-weight: 600; font-size: 13px;
}}
QPushButton#sidebar_btn {{
    background: transparent; color: {p['sidebar_text_dim']}; border: none;
    border-radius: 10px; text-align: left; padding: 0 14px;
    font-family: {FONT_FAMILY}; font-size: 13px; font-weight: 500;
    margin: 1px 10px;
}}
QPushButton#sidebar_btn:hover {{
    background-color: {p['sidebar_hover']}; color: {p['sidebar_text']};
}}
QPushButton#sidebar_btn:checked {{
    background-color: {p['sidebar_active_bg']}; color: {p['sidebar_text']};
    font-weight: 600;
}}
"""


def _page(p):
    return f"""
QFrame#page_header {{
    background-color: transparent;
    border: none;
}}
QLabel#page_title {{
    color: {p['text_primary']}; background: transparent; border: none;
    font-size: 24px; font-weight: 700; letter-spacing: -0.3px;
}}
QLabel#page_subtitle {{
    color: {p['text_secondary']}; background: transparent; border: none;
    font-size: 13px; font-weight: 400;
}}
QFrame#filter_panel {{
    background-color: {p['bg_card']};
    border: 1px solid {p['border_light']};
    border-radius: 14px;
}}
QFrame#filter_panel QLabel {{
    color: {p['text_secondary']};
    font-size: 12px;
    font-weight: 500;
}}
QFrame#dashboard_header {{
    background-color: transparent;
    border: none;
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
    border: 1px solid {p['border']}; border-radius: 10px; padding: 10px 14px;
    background-color: {p['input_bg']}; color: {p['text_primary']};
    font-size: 14px; font-family: {FONT_FAMILY};
    selection-background-color: {p['primary_light']}; selection-color: {p['text_primary']};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1.5px solid {p['primary']};
    background-color: {p['bg_card']};
}}
QLineEdit:hover, QTextEdit:hover {{ border: 1px solid {p['border_hover']}; }}
QComboBox {{
    border: 1px solid {p['border']}; border-radius: 10px; padding: 8px 14px;
    background-color: {p['input_bg']}; color: {p['text_primary']}; font-size: 14px;
}}
QComboBox:hover {{ border: 1px solid {p['border_hover']}; }}
QComboBox:focus {{ border: 1.5px solid {p['primary']}; background-color: {p['bg_card']}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox QAbstractItemView {{
    border: 1px solid {p['border']}; border-radius: 10px;
    background-color: {p['bg_card']}; selection-background-color: {p['primary_light']};
    color: {p['text_primary']}; padding: 4px;
}}
QDateEdit, QSpinBox, QDoubleSpinBox {{
    border: 1px solid {p['border']}; border-radius: 10px; padding: 8px 14px;
    background-color: {p['input_bg']}; color: {p['text_primary']}; font-size: 14px;
}}
QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1.5px solid {p['primary']};
    background-color: {p['bg_card']};
}}
QGroupBox {{
    font-weight: 600; font-size: 14px; color: {p['text_primary']};
    border: 1px solid {p['border_light']}; border-radius: 14px;
    margin-top: 16px; padding: 22px 16px 16px; background-color: {p['bg_card']};
}}
QGroupBox::title {{
    subcontrol-origin: margin; subcontrol-position: top left;
    left: 16px; padding: 0 8px; background-color: {p['bg_card']};
}}
QCheckBox {{ font-size: 13px; color: {p['text_primary']}; spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px; border: 2px solid {p['border']};
    border-radius: 5px; background-color: {p['input_bg']};
}}
QCheckBox::indicator:checked {{ background-color: {p['primary']}; border-color: {p['primary']}; }}
QTextBrowser {{
    border: 1px solid {p['border_light']}; border-radius: 12px;
    background-color: {p['bg_card']}; color: {p['text_primary']};
    padding: 14px; font-size: 13px;
}}
"""


def _buttons(p):
    return f"""
QPushButton {{
    background-color: {p['primary']};
    color: {p['text_on_primary']};
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 600;
    font-family: {FONT_FAMILY};
    min-height: 18px;
}}
QPushButton:hover {{
    background-color: {p['primary_dark']};
}}
QPushButton:pressed {{
    background-color: {p['primary_pressed']};
}}
QPushButton:disabled {{
    background-color: {p['border_light']};
    color: {p['text_secondary']};
}}
QPushButton#btn_primary {{
    background-color: {p['primary']};
    color: {p['text_on_primary']};
    border: none;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: 600;
    min-width: 120px;
}}
QPushButton#btn_primary:hover {{
    background-color: {p['primary_dark']};
}}
QPushButton#success {{
    background-color: {p['success']};
    color: {p['text_on_primary']};
    border: none;
}}
QPushButton#warning {{
    background-color: {p['warning']};
    color: {p['text_primary']};
    border: none;
}}
QPushButton#error {{
    background-color: {p['error']};
    color: white;
    border: none;
}}
QPushButton#flat {{
    background-color: {p['bg_card']};
    color: {p['text_primary']};
    border: 1px solid {p['border']};
    font-weight: 500;
}}
QPushButton#flat:hover {{
    background-color: {p['primary_light']};
    color: {p['primary_dark']};
    border-color: {p['primary']};
}}
QPushButton#ghost {{
    background-color: transparent;
    color: {p['text_secondary']};
    border: none;
    font-weight: 500;
}}
QPushButton#ghost:hover {{
    color: {p['primary']};
    background-color: {p['primary_light']};
}}
QPushButton#kanban_add {{
    background-color: transparent;
    color: {p['text_secondary']};
    border: 1.5px dashed {p['border']};
    border-radius: 10px;
    padding: 12px;
    font-weight: 500;
}}
QPushButton#kanban_add:hover {{
    border-color: {p['primary']};
    color: {p['primary']};
    background-color: {p['primary_light']};
}}
"""


def _tables(p):
    return f"""
QTableWidget, QTableView, QTreeView {{
    border: none;
    border-radius: 14px;
    background-color: {p['bg_card']};
    alternate-background-color: {p['table_alt']};
    selection-background-color: {p['primary_light']};
    selection-color: {p['text_primary']};
    gridline-color: transparent;
    font-size: 13px;
    color: {p['text_primary']};
    outline: none;
}}
QTableWidget#data_table, QTableView#data_table {{
    border: 1px solid {p['border_light']};
    background-color: {p['bg_card']};
}}
QTableWidget::item, QTableView::item {{
    padding: 12px 16px;
    color: {p['text_primary']};
    border: none;
    border-bottom: 1px solid {p['border_light']};
}}
QTableWidget::item:alternate, QTableView::item:alternate {{
    background-color: {p['table_alt']};
    color: {p['text_primary']};
}}
QTableWidget::item:selected, QTableView::item:selected {{
    background-color: {p['primary_light']};
    color: {p['text_primary']};
}}
QTableWidget::item:hover, QTableView::item:hover {{
    background-color: {p['table_hover']};
    color: {p['text_primary']};
}}
QHeaderView::section {{
    background-color: {p['table_header']};
    padding: 14px 16px;
    border: none;
    border-bottom: 1px solid {p['border']};
    font-weight: 600;
    font-size: 12px;
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
    border: 1px solid {p['border_light']}; border-radius: 12px;
    background-color: {p['bg_card']}; top: -1px; padding: 4px;
}}
QTabBar {{ background-color: transparent; border: none; }}
QTabBar::tab {{
    background: transparent; border: none;
    padding: 10px 18px; font-size: 13px; font-weight: 500;
    color: {p['text_secondary']}; font-family: {FONT_FAMILY};
    border-radius: 8px; margin: 4px 2px;
}}
QTabBar::tab:selected {{
    color: {p['primary']};
    background-color: {p['primary_light']};
    font-weight: 600;
}}
QTabBar::tab:hover:!selected {{
    color: {p['text_primary']};
    background-color: {p['table_hover']};
}}
"""


def _dialogs(p):
    return f"""
QDialog {{
    background-color: {p['bg_card']}; border: 1px solid {p['border_light']}; border-radius: 16px;
}}
QFrame#dialog_accent {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {p['primary']}, stop:1 {p['primary_dark']});
    border: none;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
    max-height: 4px;
    min-height: 4px;
}}
QWidget#dialog_body {{ background-color: {p['bg_card']}; border: none; }}
QFrame#dialog_footer {{
    background-color: {p['bg_card']}; border-top: 1px solid {p['border_light']};
    border-bottom-left-radius: 15px; border-bottom-right-radius: 15px;
}}
QMessageBox {{ background-color: {p['bg_card']}; }}
QMessageBox QLabel {{ color: {p['text_primary']}; font-size: 14px; }}
"""


def _notifications(p):
    return f"""
QFrame#notification_info {{ background-color: {p['status_new_bg']}; border-left: 3px solid {p['status_new']}; border-radius: 10px; }}
QFrame#notification_success {{ background-color: {p['status_done_bg']}; border-left: 3px solid {p['status_done']}; border-radius: 10px; }}
QFrame#notification_warning {{ background-color: {p['status_progress_bg']}; border-left: 3px solid {p['status_progress']}; border-radius: 10px; }}
QFrame#notification_error {{ background-color: {p['accent_light']}; border-left: 3px solid {p['error']}; border-radius: 10px; }}
QLabel#notification_text {{ color: {p['text_primary']}; font-weight: 600; }}
QPushButton#notification_close {{ background: transparent; color: {p['text_secondary']}; border: none; font-size: 16px; }}
QFrame#notifications_panel {{
    background-color: {p['bg_card']}; border: 1px solid {p['border_light']}; border-radius: 14px;
}}
"""


def _kanban(p):
    return f"""
QFrame#kanban_column {{ background-color: {p['kanban_col_bg']}; border-radius: 14px; border: none; }}
QFrame#kanban_column_new {{ background-color: {p['status_new_bg']}; border-radius: 14px; border: none; }}
QFrame#kanban_column_progress {{ background-color: {p['status_progress_bg']}; border-radius: 14px; border: none; }}
QFrame#kanban_column_review {{ background-color: {p['status_review_bg']}; border-radius: 14px; border: none; }}
QFrame#kanban_column_done {{ background-color: {p['status_done_bg']}; border-radius: 14px; border: none; }}
QFrame#kanban_card {{
    background-color: {p['bg_card']}; border-radius: 12px;
    border: 1px solid {p['border_light']};
}}
QFrame#kanban_card:hover {{ border: 1px solid {p['primary']}; }}
QLabel#kanban_col_title {{ font-size: 14px; font-weight: 700; color: {p['text_primary']}; }}
QLabel#card_title {{ font-size: 14px; font-weight: 600; color: {p['text_primary']}; }}
QLabel#card_project {{ font-size: 12px; color: {p['primary']}; font-weight: 500; }}
QLabel#card_developer, QLabel#card_hours {{ font-size: 12px; color: {p['text_secondary']}; }}
QFrame#stat_card {{
    background-color: {p['bg_card']}; border-radius: 14px;
    border: 1px solid {p['border_light']};
}}
QFrame#stat_card:hover {{ border-color: {p['primary']}; }}
QLabel#stat_value {{ font-size: 32px; font-weight: 700; color: {p['text_primary']}; letter-spacing: -0.5px; }}
QLabel#stat_title {{ font-size: 13px; color: {p['text_secondary']}; font-weight: 500; }}
"""
