import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QStatusBar, QLabel, QMessageBox, QWidget,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QToolBar,
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from ui.resources.styles import GLOBAL_STYLE
from ui.resources.icon_helper import get_icon, app_icon
from ui.widgets.sidebar import Sidebar
from ui.tabs.admin_tab import AdminTab
from ui.tabs.dashboard_tab import DashboardTab
from ui.tabs.developers_tab import DevelopersTab
from ui.tabs.projects_tab import ProjectsTab
from ui.tabs.tasks_tab import TasksTab
from ui.tabs.reports_tab import ReportsTab
from ui.tabs.settings_tab import SettingsTab
from ui.dialogs.about_dialog import AboutDialog


class MainWindow(QMainWindow):
    """Главное окно приложения — layout в стиле Bitrix24."""

    def __init__(self, user):
        super().__init__()
        self.user = user
        self._pages = {}
        self.init_ui()
        self.setStyleSheet(GLOBAL_STYLE)

    def init_ui(self):
        self.setWindowTitle('KABAN:manager')
        self.setWindowIcon(app_icon())
        self.setMinimumSize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = Sidebar(self.user)
        self.sidebar.navigated.connect(self._switch_page)
        root_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.stack.setObjectName('page_content')
        root_layout.addWidget(self.stack, stretch=1)

        self._build_pages()
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.showMaximized()

    def _build_pages(self):
        self.dashboard_tab = DashboardTab(self.user)
        self._add_page('dashboard', self.dashboard_tab)

        if self.user.role == 'developer':
            self.projects_tab = ProjectsTab(self.user)
            self.tasks_tab = TasksTab(self.user)
            self._add_page('projects', self.projects_tab)
            self._add_page('tasks', self.tasks_tab)
        else:
            self.developers_tab = DevelopersTab(self.user)
            self.projects_tab = ProjectsTab(self.user)
            self.tasks_tab = TasksTab(self.user)
            self.reports_tab = ReportsTab(self.user)
            self.settings_tab = SettingsTab(self.user)
            self._add_page('developers', self.developers_tab)
            self._add_page('projects', self.projects_tab)
            self._add_page('tasks', self.tasks_tab)
            self._add_page('reports', self.reports_tab)
            self._add_page('settings', self.settings_tab)

        if self.user.role == 'admin':
            self.admin_tab = AdminTab(self.user)
            self._add_page('admin', self.admin_tab)

        keys = self.sidebar.item_keys()
        for i, key in enumerate(keys):
            if key in self._pages:
                self.stack.addWidget(self._pages[key])
        self.stack.setCurrentIndex(0)

    def _add_page(self, key, widget):
        self._pages[key] = widget

    def _switch_page(self, index):
        if 0 <= index < self.stack.count():
            self.stack.setCurrentIndex(index)
            self.sidebar.set_active_index(index)

    @property
    def tab_widget(self):
        """Совместимость с кодом, который ищет tab_widget (дашборд)."""
        return _TabWidgetProxy(self)

    def _current_tab(self):
        widget = self.stack.currentWidget()
        return widget

    def _switch_to_key(self, key):
        keys = self.sidebar.item_keys()
        if key in keys:
            idx = keys.index(key)
            self._switch_page(idx)

    def create_menu(self):
        file_menu = self.menuBar().addMenu('Файл')

        export_csv_action = QAction(get_icon('export'), 'Экспорт в CSV', self)
        export_csv_action.setShortcut('Ctrl+1')
        export_csv_action.setStatusTip('Экспорт данных в CSV')
        export_csv_action.triggered.connect(self.export_to_csv)

        export_excel_action = QAction(get_icon('export'), 'Экспорт в Excel', self)
        export_excel_action.setShortcut('Ctrl+2')
        export_excel_action.setStatusTip('Экспорт данных в Excel')
        export_excel_action.triggered.connect(self.export_to_excel)

        file_menu.addAction(export_csv_action)
        file_menu.addAction(export_excel_action)

        exit_action = QAction(app_icon(), 'Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Выход из приложения')
        exit_action.triggered.connect(self.close)

        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = self.menuBar().addMenu('Правка')

        add_action = QAction(get_icon('add'), 'Добавить', self)
        add_action.setShortcut('Ctrl+N')
        add_action.setStatusTip('Добавить новую запись')
        add_action.triggered.connect(self.add_item)

        edit_action = QAction(get_icon('edit'), 'Редактировать', self)
        edit_action.setShortcut('Ctrl+E')
        edit_action.setStatusTip('Редактировать выбранную запись')
        edit_action.triggered.connect(self.edit_item)

        delete_action = QAction(get_icon('delete'), 'Удалить', self)
        delete_action.setShortcut('Delete')
        delete_action.setStatusTip('Удалить выбранную запись')
        delete_action.triggered.connect(self.delete_item)

        refresh_action = QAction(get_icon('refresh'), 'Обновить', self)
        refresh_action.setShortcut('F5')
        refresh_action.setStatusTip('Обновить данные')
        refresh_action.triggered.connect(self.refresh_data)

        edit_menu.addAction(add_action)
        edit_menu.addAction(edit_action)
        edit_menu.addAction(delete_action)
        edit_menu.addSeparator()
        edit_menu.addAction(refresh_action)

        view_menu = self.menuBar().addMenu('Вид')

        fullscreen_action = QAction('Полноэкранный режим', self)
        fullscreen_action.setShortcut('F11')
        fullscreen_action.setCheckable(True)
        fullscreen_action.setStatusTip('Переключить полноэкранный режим')
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        help_menu = self.menuBar().addMenu('Справка')

        about_action = QAction(get_icon('about'), 'О программе', self)
        about_action.setStatusTip('Информация о программе')
        about_action.triggered.connect(self.show_about)

        help_action = QAction(get_icon('info'), 'Справка', self)
        help_action.setShortcut('F1')
        help_action.setStatusTip('Показать справку')
        help_action.triggered.connect(self.show_help)

        help_menu.addAction(about_action)
        help_menu.addAction(help_action)

    def create_toolbar(self):
        main_toolbar = QToolBar('Основная панель', self)
        main_toolbar.setIconSize(QSize(20, 20))
        main_toolbar.setMovable(False)
        self.addToolBar(main_toolbar)

        for icon_name, tip, slot in [
            ('add', 'Добавить новую запись', self.add_item),
            ('edit', 'Редактировать выбранную запись', self.edit_item),
            ('delete', 'Удалить выбранную запись', self.delete_item),
            ('refresh', 'Обновить данные', self.refresh_data),
            ('export', 'Экспорт данных', self.export_to_csv),
        ]:
            action = QAction(get_icon(icon_name), tip.split()[0], self)
            action.setStatusTip(tip)
            action.triggered.connect(slot)
            main_toolbar.addAction(action)
            if icon_name == 'delete':
                main_toolbar.addSeparator()

    def create_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        user_label = QLabel(f"  {self.user.full_name}  ·  {self.user.role}  ")
        user_label.setFont(QFont('Segoe UI', 10))
        self.statusbar.addPermanentWidget(user_label)

        version_label = QLabel("  v1.0.0  ")
        version_label.setFont(QFont('Segoe UI', 10))
        self.statusbar.addPermanentWidget(version_label)
        self.statusbar.showMessage('Готово', 3000)

    def add_item(self):
        current_tab = self._current_tab()
        if hasattr(current_tab, 'add_item'):
            current_tab.add_item()
        else:
            self.statusbar.showMessage('Функция добавления не поддерживается на этой вкладке', 3000)

    def edit_item(self):
        current_tab = self._current_tab()
        if hasattr(current_tab, 'edit_item'):
            current_tab.edit_item()
        else:
            self.statusbar.showMessage('Функция редактирования не поддерживается на этой вкладке', 3000)

    def delete_item(self):
        current_tab = self._current_tab()
        if hasattr(current_tab, 'delete_item'):
            current_tab.delete_item()
        else:
            self.statusbar.showMessage('Функция удаления не поддерживается на этой вкладке', 3000)

    def refresh_data(self):
        current_tab = self._current_tab()
        if hasattr(current_tab, 'refresh_data'):
            current_tab.refresh_data()
            self.statusbar.showMessage('Данные обновлены', 3000)
        else:
            self.statusbar.showMessage('Функция обновления не поддерживается на этой вкладке', 3000)

    def export_to_csv(self):
        current_tab = self._current_tab()
        if hasattr(current_tab, 'export_to_csv'):
            current_tab.export_to_csv()
        else:
            self.statusbar.showMessage('Функция экспорта в CSV не поддерживается на этой вкладке', 3000)

    def export_to_excel(self):
        current_tab = self._current_tab()
        if hasattr(current_tab, 'export_to_excel'):
            current_tab.export_to_excel()
        else:
            self.statusbar.showMessage('Функция экспорта в Excel не поддерживается на этой вкладке', 3000)

    def toggle_fullscreen(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showMaximized()

    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def show_help(self):
        QMessageBox.information(self, 'Справка', 'Справочная информация о программе KABAN:manager')

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Выход', 'Вы уверены, что хотите выйти?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class _TabWidgetProxy:
    """Прокси для совместимости dashboard_tab.show_all_tasks."""

    def __init__(self, main_window):
        self._mw = main_window

    def count(self):
        return self._mw.stack.count()

    def tabText(self, index):
        keys = self._mw.sidebar.item_keys()
        labels = dict(Sidebar._ALL_ITEMS)
        if index < len(keys):
            return labels.get(keys[index], ('', '', ''))[2]
        return ''

    def setCurrentIndex(self, index):
        self._mw._switch_page(index)

    def parent(self):
        return None
