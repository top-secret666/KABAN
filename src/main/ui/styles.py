PRIMARY_COLOR = "#1976D2"
SECONDARY_COLOR = "#424242"
SUCCESS_COLOR = "#4CAF50"
WARNING_COLOR = "#FFC107"
ERROR_COLOR = "#F44336"
INFO_COLOR = "#2196F3"
LIGHT_COLOR = "#F5F5F5"
DARK_COLOR = "#212121"

MAIN_WINDOW_STYLE = f"""
QMainWindow {{
    background-color: {LIGHT_COLOR};
}}

QMenuBar {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
}}

QMenuBar::item {{
    background-color: transparent;
    padding: 8px 12px;
}}

QMenuBar::item:selected {{
    background-color: rgba(255, 255, 255, 0.2);
}}

QMenu {{
    background-color: white;
    border: 1px solid #ddd;
}}

QMenu::item {{
    padding: 6px 25px 6px 20px;
}}

QMenu::item:selected {{
    background-color: {PRIMARY_COLOR};
    color: white;
}}

QStatusBar {{
    background-color: {LIGHT_COLOR};
    color: {DARK_COLOR};
    border-top: 1px solid #ddd;
}}

QTabWidget::pane {{
    border: 1px solid #ddd;
    background-color: white;
}}

QTabBar::tab {{
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-bottom: none;
    padding: 8px 15px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: white;
    border-bottom: 2px solid {PRIMARY_COLOR};
}}

QTabBar::tab:!selected {{
    margin-top: 2px;
}}
"""

FORM_STYLE = f"""
QWidget {{
    background-color: white;
}}

QLabel {{
    color: {DARK_COLOR};
    font-size: 12px;
}}

QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {{
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 8px;
    background-color: white;
    selection-background-color: {PRIMARY_COLOR};
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1px solid {PRIMARY_COLOR};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: url(ui/resources/icons/dropdown.png);
    width: 12px;
    height: 12px;
}}

QDateEdit::drop-down {{
    border: none;
    width: 20px;
}}

QGroupBox {{
    font-weight: bold;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 15px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
}}
"""

BUTTON_STYLE = f"""
QPushButton {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #1565C0;
}}

QPushButton:pressed {{
    background-color: #0D47A1;
}}

QPushButton:disabled {{
    background-color: #BDBDBD;
    color: #757575;
}}

QPushButton#success {{
    background-color: {SUCCESS_COLOR};
}}

QPushButton#success:hover {{
    background-color: #388E3C;
}}

QPushButton#warning {{
    background-color: {WARNING_COLOR};
    color: {DARK_COLOR};
}}

QPushButton#warning:hover {{
    background-color: #FFA000;
}}

QPushButton#error {{
    background-color: {ERROR_COLOR};
}}

QPushButton#error:hover {{
    background-color: #D32F2F;
}}

QPushButton#flat {{
    background-color: transparent;
    color: {PRIMARY_COLOR};
    border: 1px solid {PRIMARY_COLOR};
}}

QPushButton#flat:hover {{
    background-color: rgba(25, 118, 210, 0.1);
}}
"""

TABLE_STYLE = f"""
QTableView, QTreeView {{
    border: 1px solid #ddd;
    background-color: white;
    alternate-background-color: #f9f9f9;
    selection-background-color: {PRIMARY_COLOR};
    selection-color: white;
}}

QTableView::item, QTreeView::item {{
    padding: 5px;
}}

QHeaderView::section {{
    background-color: #f0f0f0;
    padding: 5px;
    border: 1px solid #ddd;
    font-weight: bold;
}}

QTableView::item:selected, QTreeView::item:selected {{
    background-color: {PRIMARY_COLOR};
}}
"""

DIALOG_STYLE = f"""
QDialog {{
    background-color: white;
}}

QDialog QLabel {{
    color: {DARK_COLOR};
}}

QDialog QPushButton {{
    min-width: 80px;
}}

QMessageBox {{
    background-color: white;
}}

QMessageBox QLabel {{
    color: {DARK_COLOR};
}}

QInputDialog {{
    background-color: white;
}}
"""

NOTIFICATION_STYLE = f"""
QFrame#notification_info {{
    background-color: {INFO_COLOR};
    color: white;
    border-radius: 4px;
}}

QFrame#notification_success {{
    background-color: {SUCCESS_COLOR};
    color: white;
    border-radius: 4px;
}}

QFrame#notification_warning {{
    background-color: {WARNING_COLOR};
    color: {DARK_COLOR};
    border-radius: 4px;
}}

QFrame#notification_error {{
    background-color: {ERROR_COLOR};
    color: white;
    border-radius: 4px;
}}

QLabel#notification_text {{
    color: inherit;
    font-weight: bold;
}}

QPushButton#notification_close {{
    background-color: transparent;
    color: inherit;
    border: none;
    font-weight: bold;
    font-size: 16px;
}}
"""

GLOBAL_STYLE = MAIN_WINDOW_STYLE + FORM_STYLE + BUTTON_STYLE + TABLE_STYLE + DIALOG_STYLE + NOTIFICATION_STYLE
