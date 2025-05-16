from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QAction, QMenu, QToolBar,
                            QStatusBar, QLabel, QMessageBox, QWidget, QVBoxLayout)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from .resources.styles import GLOBAL_STYLE
from .tabs.dashboard_tab import DashboardTab
from .tabs.developers_tab import DevelopersTab
from .tabs.projects_tab import ProjectsTab
from .tabs.tasks_tab import TasksTab
from .tabs.reports_tab import ReportsTab
from .tabs.settings_tab import SettingsTab
from .dialog.about_dialog import AboutDialog

class MainWindow(QMainWindow):
    """
    Главное окно приложения
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.init_ui()
        self.setStyleSheet(GLOBAL_STYLE)
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('KABAN:manager')
        self.setWindowIcon(QIcon('src/main/ui/resources/icons/kaban.png'))
        self.setMinimumSize(1200, 800)
        
        # Создание центрального виджета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Создание вкладок
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)
        
        # Добавление вкладок
        self.dashboard_tab = DashboardTab(self.user)
        self.developers_tab = DevelopersTab(self.user)
        self.projects_tab = ProjectsTab(self.user)
        self.tasks_tab = TasksTab(self.user)
        self.reports_tab = ReportsTab(self.user)
        self.settings_tab = SettingsTab(self.user)
        
        self.tab_widget.addTab(self.dashboard_tab, QIcon('src/main/ui/resources/icons/kaban.png'), 'Дашборд')
        self.tab_widget.addTab(self.developers_tab, QIcon('src/main/ui/resources/icons/kaban.png'), 'Разработчики')
        self.tab_widget.addTab(self.projects_tab, QIcon('src/main/ui/resources/icons/kaban.png'), 'Проекты')
        self.tab_widget.addTab(self.tasks_tab, QIcon('src/main/ui/resources/icons/kaban.png'), 'Задачи')
        self.tab_widget.addTab(self.reports_tab, QIcon('src/main/ui/resources/icons/kaban.png'), 'Отчеты')
        self.tab_widget.addTab(self.settings_tab, QIcon('src/main/ui/resources/icons/kaban.png'), 'Настройки')
        
        main_layout.addWidget(self.tab_widget)
        
        # Создание меню
        self.create_menu()
        
        # Создание панели инструментов
        self.create_toolbar()
        
        # Создание строки состояния
        self.create_statusbar()
        
        # Отображение окна
        self.showMaximized()
    
    def create_menu(self):
        """
        Создание главного меню
        """
        # Меню "Файл"
        file_menu = self.menuBar().addMenu('Файл')
        
        # Действие "Экспорт"
        export_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Экспорт', self)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Экспорт данных')
        
        # Подменю "Экспорт"
        export_menu = QMenu('Экспорт', self)
        export_csv_action = QAction('Экспорт в CSV', self)
        export_csv_action.triggered.connect(self.export_to_csv)
        export_excel_action = QAction('Экспорт в Excel', self)
        export_excel_action.triggered.connect(self.export_to_excel)
        
        export_menu.addAction(export_csv_action)
        export_menu.addAction(export_excel_action)
        export_action.setMenu(export_menu)
        
        # Действие "Импорт"
        import_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Импорт', self)
        import_action.setShortcut('Ctrl+I')
        import_action.setStatusTip('Импорт данных')
        import_action.triggered.connect(self.import_data)
        
        # Действие "Выход"
        exit_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Выход из приложения')
        exit_action.triggered.connect(self.close)
        
        file_menu.addAction(export_action)
        file_menu.addAction(import_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        
        # Меню "Правка"
        edit_menu = self.menuBar().addMenu('Правка')
        
        # Действие "Добавить"
        add_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Добавить', self)
        add_action.setShortcut('Ctrl+N')
        add_action.setStatusTip('Добавить новую запись')
        add_action.triggered.connect(self.add_item)
        
        # Действие "Редактировать"
        edit_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Редактировать', self)
        edit_action.setShortcut('Ctrl+E')
        edit_action.setStatusTip('Редактировать выбранную запись')
        edit_action.triggered.connect(self.edit_item)
        
        # Действие "Удалить"
        delete_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Удалить', self)
        delete_action.setShortcut('Delete')
        delete_action.setStatusTip('Удалить выбранную запись')
        delete_action.triggered.connect(self.delete_item)
        
        # Действие "Обновить"
        refresh_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Обновить', self)
        refresh_action.setShortcut('F5')
        refresh_action.setStatusTip('Обновить данные')
        refresh_action.triggered.connect(self.refresh_data)
        
        edit_menu.addAction(add_action)
        edit_menu.addAction(edit_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(refresh_action)
        
        # Меню "Вид"
        view_menu = self.menuBar().addMenu('Вид')
        
        # Действие "Полноэкранный режим"
        fullscreen_action = QAction('Полноэкранный режим', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.setStatusTip('Переключить полноэкранный режим')
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        view_menu.addAction(fullscreen_action)
        
        # Меню "Справка"
        help_menu = self.menuBar().addMenu('Справка')
        
        # Действие "О программе"
        about_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'О программе', self)
        about_action.setStatusTip('Информация о программе')
        about_action.triggered.connect(self.show_about)
        
        # Действие "Справка"
        help_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Справка', self)
        help_action.setShortcut('F1')
        help_action.setStatusTip('Показать справку')
        help_action.triggered.connect(self.show_help)
        
        help_menu.addAction(about_action)
        help_menu.addAction(help_action)
    
    def create_toolbar(self):
        """
        Создание панели инструментов
        """
        # Основная панель инструментов
        main_toolbar = QToolBar('Основная панель', self)
        main_toolbar.setIconSize(QSize(24, 24))
        main_toolbar.setMovable(False)
        self.addToolBar(main_toolbar)
        
        # Добавление действий
        add_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Добавить', self)
        add_action.setStatusTip('Добавить новую запись')
        add_action.triggered.connect(self.add_item)
        
        edit_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Редактировать', self)
        edit_action.setStatusTip('Редактировать выбранную запись')
        edit_action.triggered.connect(self.edit_item)
        
        delete_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Удалить', self)
        delete_action.setStatusTip('Удалить выбранную запись')
        delete_action.triggered.connect(self.delete_item)
        
        refresh_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Обновить', self)
        refresh_action.setStatusTip('Обновить данные')
        refresh_action.triggered.connect(self.refresh_data)
        
        export_action = QAction(QIcon('src/main/ui/resources/icons/kaban.png'), 'Экспорт', self)
        export_action.setStatusTip('Экспорт данных')
        export_action.triggered.connect(self.export_to_csv)
        
        main_toolbar.addAction(add_action)
        main_toolbar.addAction(edit_action)
        main_toolbar.addAction(delete_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(refresh_action)
        main_toolbar.addSeparator()
        main_toolbar.addAction(export_action)
    
    def create_statusbar(self):
        """
        Создание строки состояния
        """
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Добавление информации о пользователе
        user_label = QLabel(f"Пользователь: {self.user.full_name} ({self.user.role})")
        self.statusbar.addPermanentWidget(user_label)
        
        # Добавление информации о версии
        version_label = QLabel("Версия 1.0.0")
        self.statusbar.addPermanentWidget(version_label)
        
        # Установка начального сообщения
        self.statusbar.showMessage('Готово', 3000)
    
    def add_item(self):
        """
        Добавление новой записи
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'add_item'):
            current_tab.add_item()
        else:
            self.statusbar.showMessage('Функция добавления не поддерживается на этой вкладке', 3000)
    
    def edit_item(self):
        """
        Редактирование выбранной записи
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'edit_item'):
            current_tab.edit_item()
        else:
            self.statusbar.showMessage('Функция редактирования не поддерживается на этой вкладке', 3000)
    
    def delete_item(self):
        """
        Удаление выбранной записи
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'delete_item'):
            current_tab.delete_item()
        else:
            self.statusbar.showMessage('Функция удаления не поддерживается на этой вкладке', 3000)
    
    def refresh_data(self):
        """
        Обновление данных
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'refresh_data'):
            current_tab.refresh_data()
            self.statusbar.showMessage('Данные обновлены', 3000)
        else:
            self.statusbar.showMessage('Функция обновления не поддерживается на этой вкладке', 3000)
    
    def export_to_csv(self):
        """
        Экспорт данных в CSV
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'export_to_csv'):
            current_tab.export_to_csv()
        else:
            self.statusbar.showMessage('Функция экспорта в CSV не поддерживается на этой вкладке', 3000)
    
    def export_to_excel(self):
        """
        Экспорт данных в Excel
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'export_to_excel'):
            current_tab.export_to_excel()
        else:
            self.statusbar.showMessage('Функция экспорта в Excel не поддерживается на этой вкладке', 3000)
    
    def import_data(self):
        """
        Импорт данных
        """
        current_tab = self.tab_widget.currentWidget()
        if hasattr(current_tab, 'import_data'):
            current_tab.import_data()
        else:
            self.statusbar.showMessage('Функция импорта не поддерживается на этой вкладке', 3000)
    
    def toggle_fullscreen(self, checked):
        """
        Переключение полноэкранного режима
        """
        if checked:
            self.showFullScreen()
        else:
            self.showMaximized()
    
    def show_about(self):
        """
        Показать информацию о программе
        """
        about_dialog = AboutDialog(self)
        about_dialog.exec_()
    
    def show_help(self):
        """
        Показать справку
        """
        QMessageBox.information(self, 'Справка', 'Справочная информация о программе KABAN:manager')
    
    def closeEvent(self, event):
        """
        Обработка закрытия окна
        """
        reply = QMessageBox.question(
            self, 'Выход', 'Вы уверены, что хотите выйти?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
