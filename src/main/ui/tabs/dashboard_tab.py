from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QFrame, QScrollArea, QSizePolicy, QGridLayout)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

from src.main.service.controllers import ProjectController, TaskController, DeveloperController, NotificationController

class DashboardTab(QWidget):
    """
    Вкладка "Дашборд" - главная страница приложения
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.project_controller = ProjectController()
        self.task_controller = TaskController()
        self.developer_controller = DeveloperController()
        self.notification_controller = NotificationController()
        self.init_ui()
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Заголовок
        header_layout = QHBoxLayout()
        
        title_label = QLabel(f"Добро пожаловать, {self.user.full_name}!")
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        header_layout.addWidget(title_label)
        
        refresh_button = QPushButton("Обновить")
        refresh_button.setIcon(QIcon('ui/resources/icons/refresh.png'))
        refresh_button.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_button, alignment=Qt.AlignRight)
        
        main_layout.addLayout(header_layout)
        
        # Создание области прокрутки
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Создание виджета для размещения содержимого
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(20)
        
        # Добавление виджетов с информацией
        scroll_layout.addLayout(self.create_stats_widgets())
        scroll_layout.addWidget(self.create_recent_tasks_widget())
        scroll_layout.addWidget(self.create_notifications_widget())
        
        # Добавление растягивающегося пространства в конец
        scroll_layout.addStretch()
        
        # Установка виджета содержимого для области прокрутки
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def create_stats_widgets(self):
        """
        Создание виджетов со статистикой
        """
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        
        # Получение данных
        projects_result = self.project_controller.get_all_projects()
        tasks_result = self.task_controller.get_all_tasks()
        developers_result = self.developer_controller.get_all_developers()
        
        projects = projects_result['data'] if projects_result['success'] else []
        tasks = tasks_result['data'] if tasks_result['success'] else []
        developers = developers_result['data'] if developers_result['success'] else []
        
        # Статистика по проектам
        projects_widget = self.create_stat_card(
            "Проекты",
            len(projects),
            "ui/resources/icons/project.png",
            "#1976D2"
        )
        
        # Статистика по задачам
        tasks_widget = self.create_stat_card(
            "Задачи",
            len(tasks),
            "ui/resources/icons/task.png",
            "#4CAF50"
        )
        
        # Статистика по разработчикам
        developers_widget = self.create_stat_card(
            "Разработчики",
            len(developers),
            "ui/resources/icons/developer.png",
            "#FF9800"
        )
        
        # Статистика по просроченным задачам
        overdue_tasks = [task for task in tasks if task.status != 'завершено' and hasattr(task, 'project_deadline') and task.project_deadline < self.get_current_date()]
        overdue_widget = self.create_stat_card(
            "Просроченные задачи",
            len(overdue_tasks),
            "ui/resources/icons/warning.png",
            "#F44336"
        )
        
        # Добавление виджетов в сетку
        stats_layout.addWidget(projects_widget, 0, 0)
        stats_layout.addWidget(tasks_widget, 0, 1)
        stats_layout.addWidget(developers_widget, 1, 0)
        stats_layout.addWidget(overdue_widget, 1, 1)
        
        return stats_layout
    
    def create_stat_card(self, title, value, icon_path, color):
        """
        Создание карточки со статистикой
        """
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setFrameShadow(QFrame.Raised)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setMinimumHeight(120)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 8px;
                border-left: 5px solid {color};
            }}
        """)
        
        layout = QHBoxLayout(card)
        
        # Иконка
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(48, 48)))
        layout.addWidget(icon_label)
        
        # Информация
        info_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 12))
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont('Arial', 24, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(value_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        return card
    
    def create_recent_tasks_widget(self):
        """
        Создание виджета с последними задачами
        """
        # Создание рамки
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        # Заголовок
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Последние задачи")
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        header_layout.addWidget(title_label)
        
        view_all_button = QPushButton("Показать все")
        view_all_button.setObjectName("flat")
        view_all_button.clicked.connect(self.show_all_tasks)
        header_layout.addWidget(view_all_button, alignment=Qt.AlignRight)
        
        layout.addLayout(header_layout)
        
        # Получение последних задач
        tasks_result = self.task_controller.get_all_tasks()
        tasks = tasks_result['data'] if tasks_result['success'] else []
        
        # Сортировка задач по дате создания (в обратном порядке)
        tasks.sort(key=lambda x: x.created_at if hasattr(x, 'created_at') else '', reverse=True)
        
        # Отображение только 5 последних задач
        recent_tasks = tasks[:5]
        
        if recent_tasks:
            for task in recent_tasks:
                task_widget = self.create_task_item(task)
                layout.addWidget(task_widget)
        else:
            no_tasks_label = QLabel("Нет задач")
            no_tasks_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_tasks_label)
        
        return frame
    
    def create_task_item(self, task):
        """
        Создание элемента задачи
        """
        item = QFrame()
        item.setFrameShape(QFrame.StyledPanel)
        item.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                margin: 4px 0;
            }
        """)
        
        layout = QVBoxLayout(item)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Заголовок задачи
        title_layout = QHBoxLayout()
        
        description_label = QLabel(task.description)
        description_label.setFont(QFont('Arial', 12, QFont.Bold))
        title_layout.addWidget(description_label)
        
        # Статус задачи
        status_label = QLabel(task.status)
        status_color = {
            'новая': '#2196F3',
            'в работе': '#FF9800',
            'на проверке': '#9C27B0',
            'завершено': '#4CAF50'
        }.get(task.status, '#757575')
        
        status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color};
                color: white;
                border-radius: 4px;
                padding: 2px 8px;
            }}
        """)
        title_layout.addWidget(status_label, alignment=Qt.AlignRight)
        
        layout.addLayout(title_layout)
        
        # Информация о проекте и разработчике
        info_layout = QHBoxLayout()
        
        project_name = getattr(task, 'project_name', 'Неизвестный проект')
        project_label = QLabel(f"Проект: {project_name}")
        info_layout.addWidget(project_label)
        
        developer_name = getattr(task, 'developer_name', 'Не назначен')
        developer_label = QLabel(f"Разработчик: {developer_name}")
        info_layout.addWidget(developer_label)
        
        # Часы работы
        hours_label = QLabel(f"Часы: {task.hours_worked}")
        info_layout.addWidget(hours_label, alignment=Qt.AlignRight)
        
        layout.addLayout(info_layout)
        
        return item
    
    def create_notifications_widget(self):
        """
        Создание виджета с уведомлениями
        """
        # Создание рамки
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        # Заголовок
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Уведомления")
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        header_layout.addWidget(title_label)
        
        mark_all_button = QPushButton("Отметить все как прочитанные")
        mark_all_button.setObjectName("flat")
        mark_all_button.clicked.connect(self.mark_all_notifications_as_read)
        header_layout.addWidget(mark_all_button, alignment=Qt.AlignRight)
        
        layout.addLayout(header_layout)
        
        # Получение уведомлений
        notifications_result = self.notification_controller.get_all_notifications(limit=5, only_unread=True)
        notifications = notifications_result['data'] if notifications_result['success'] else []
        
        if notifications:
            for notification in notifications:
                notification_widget = self.create_notification_item(notification)
                layout.addWidget(notification_widget)
        else:
            no_notifications_label = QLabel("Нет новых уведомлений")
            no_notifications_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(no_notifications_label)
        
        return frame
    
    def create_notification_item(self, notification):
        """
        Создание элемента уведомления
        """
        item = QFrame()
        item.setObjectName(f"notification_{notification.type}")
        item.setFrameShape(QFrame.StyledPanel)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Иконка уведомления
        icon_path = {
            'info': 'ui/resources/icons/info.png',
            'success': 'ui/resources/icons/success.png',
            'warning': 'ui/resources/icons/warning.png',
            'error': 'ui/resources/icons/error.png'
        }.get(notification.type, 'ui/resources/icons/info.png')
        
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(24, 24)))
        layout.addWidget(icon_label)
        
        # Текст уведомления
        text_layout = QVBoxLayout()
        
        title_label = QLabel(notification.title)
        title_label.setObjectName("notification_text")
        title_label.setFont(QFont('Arial', 12, QFont.Bold))
        
        message_label = QLabel(notification.message)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Кнопка закрытия
        close_button = QPushButton("×")
        close_button.setObjectName("notification_close")
        close_button.setFixedSize(24, 24)
        close_button.clicked.connect(lambda: self.mark_notification_as_read(notification.id))
        layout.addWidget(close_button, alignment=Qt.AlignTop)
        
        return item
    
    def show_all_tasks(self):
        """
        Показать все задачи (переключение на вкладку задач)
        """
        # Находим индекс вкладки с задачами и переключаемся на нее
        parent = self.parent()
        if parent:
            tab_widget = parent.parent()
            for i in range(tab_widget.count()):
                if tab_widget.tabText(i) == 'Задачи':
                    tab_widget.setCurrentIndex(i)
                    break
    
    def mark_notification_as_read(self, notification_id):
        """
        Отметить уведомление как прочитанное
        """
        result = self.notification_controller.mark_as_read(notification_id)
        if result['success']:
            self.refresh_data()
    
    def mark_all_notifications_as_read(self):
        """
        Отметить все уведомления как прочитанные
        """
        result = self.notification_controller.mark_all_as_read()
        if result['success']:
            self.refresh_data()
    
    def get_current_date(self):
        """
        Получение текущей даты в формате YYYY-MM-DD
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')
    
    def refresh_data(self):
        """
        Обновление данных на дашборде
        """
        # Удаляем все виджеты из layout
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Инициализируем интерфейс заново
        self.init_ui()
