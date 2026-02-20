from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                            QTabWidget, QTextBrowser)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSize

class AboutDialog(QDialog):
    """
    Диалог "О программе"
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('О программе')
        self.setWindowIcon(QIcon('ui/resources/icons/about.png'))
        self.setMinimumSize(600, 400)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)
        
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Верхняя часть с логотипом и названием
        header_layout = QHBoxLayout()
        
        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap('ui/resources/icons/logo.png')
        logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label)
        
        # Информация о программе
        info_layout = QVBoxLayout()
        
        title_label = QLabel('KABAN:manager')
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        
        version_label = QLabel('Версия 1.0.0')
        version_label.setFont(QFont('Arial', 12))
        
        description_label = QLabel('Система управления проектами и задачами для команд разработчиков')
        description_label.setWordWrap(True)
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(version_label)
        info_layout.addWidget(description_label)
        
        header_layout.addLayout(info_layout)
        main_layout.addLayout(header_layout)
        
        # Вкладки с информацией
        tab_widget = QTabWidget()
        
        # Вкладка "О программе"
        about_tab = QTextBrowser()
        about_tab.setOpenExternalLinks(True)
        about_tab.setHtml("""
            <h2>KABAN:manager</h2>
            <p>KABAN:manager - это система управления проектами и задачами, разработанная для команд разработчиков программного обеспечения.</p>
            <p>Основные возможности:</p>
            <ul>
                <li>Управление проектами и задачами</li>
                <li>Отслеживание времени работы</li>
                <li>Контроль сроков выполнения</li>
                <li>Расчет стоимости проектов</li>
                <li>Формирование отчетов</li>
                <li>Система уведомлений</li>
            </ul>
            <p>Программа разработана с использованием Python и PyQt5.</p>
        """)
        
        # Вкладка "Авторы"
        authors_tab = QTextBrowser()
        authors_tab.setHtml("""
            <h2>Авторы</h2>
            <p>Программа разработана командой разработчиков:</p>
            <ul>
                <li>Иванов Иван - руководитель проекта</li>
                <li>Петров Петр - ведущий разработчик</li>
                <li>Сидорова Анна - дизайнер интерфейса</li>
                <li>Козлов Алексей - тестировщик</li>
            </ul>
            <p>© 2023 Все права защищены</p>
        """)
        
        # Вкладка "Лицензия"
        license_tab = QTextBrowser()
        license_tab.setHtml("""
            <h2>Лицензия</h2>
            <p>Данное программное обеспечение распространяется под лицензией MIT.</p>
            <p>Copyright (c) 2023 KABAN:manager Team</p>
            <p>Permission is hereby granted, free of charge, to any person obtaining a copy
            of this software and associated documentation files (the "Software"), to deal
            in the Software without restriction, including without limitation the rights
            to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the Software is
            furnished to do so, subject to the following conditions:</p>
            <p>The above copyright notice and this permission notice shall be included in all
            copies or substantial portions of the Software.</p>
            <p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
            IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
            FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
            AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
            LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
            SOFTWARE.</p>
        """)
        
        tab_widget.addTab(about_tab, 'О программе')
        tab_widget.addTab(authors_tab, 'Авторы')
        tab_widget.addTab(license_tab, 'Лицензия')
        
        main_layout.addWidget(tab_widget)
        
        # Кнопка закрытия
        buttons_layout = QHBoxLayout()
        
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.accept)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_button)
        
        main_layout.addLayout(buttons_layout)
