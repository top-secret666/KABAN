from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QTabWidget, QTextBrowser, QPushButton, QLabel,
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from ui.dialogs.base_dialog import BaseDialog
from ui.resources.icon_helper import get_icon
from ui.resources.theme_manager import current_palette


class AboutDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent, 'О программе')
        self.setWindowIcon(get_icon('about'))
        self.setMinimumSize(620, 480)
        self._build()

    def _build(self):
        p = current_palette()
        header_layout = QHBoxLayout()
        header_layout.setSpacing(20)

        logo_label = QLabel()
        logo_pixmap = QPixmap('ui/resources/icons/logo.png')
        logo_label.setPixmap(logo_pixmap.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label)

        info_layout = QVBoxLayout()
        title_label = QLabel('KABAN:manager')
        title_label.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title_label.setStyleSheet(f'color: {p["text_primary"]}; background: transparent;')
        version_label = QLabel('Версия 1.0.0')
        version_label.setStyleSheet(f'color: {p["primary"]}; font-weight: 600; background: transparent;')
        description_label = QLabel('Система управления проектами и задачами')
        description_label.setWordWrap(True)
        description_label.setStyleSheet(f'color: {p["text_secondary"]}; background: transparent;')
        info_layout.addWidget(title_label)
        info_layout.addWidget(version_label)
        info_layout.addWidget(description_label)
        header_layout.addLayout(info_layout)
        self.body_layout.addLayout(header_layout)

        tab_widget = QTabWidget()
        about_tab = QTextBrowser()
        about_tab.setOpenExternalLinks(True)
        about_tab.setHtml("""
            <h2>KABAN:manager</h2>
            <p>Система управления проектами и задачами.</p>
            <ul>
                <li>Управление проектами и задачами</li>
                <li>Kanban-доска и дашборд</li>
                <li>Отчёты и уведомления</li>
                <li>Тёмная тема и настройка фона</li>
            </ul>
        """)
        authors_tab = QTextBrowser()
        authors_tab.setHtml('<h2>Команда</h2><p>KABAN:manager Team</p>')
        license_tab = QTextBrowser()
        license_tab.setHtml('<h2>MIT License</h2><p>Copyright (c) 2023 KABAN:manager Team</p>')
        tab_widget.addTab(about_tab, 'О программе')
        tab_widget.addTab(authors_tab, 'Авторы')
        tab_widget.addTab(license_tab, 'Лицензия')
        self.body_layout.addWidget(tab_widget)

        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.accept)
        self.add_footer_button(close_button)
