from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QScrollArea, QSizePolicy, QGridLayout, QTabWidget,
                             QGraphicsDropShadowEffect, QSpacerItem)
from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from controllers import ProjectController, TaskController, DeveloperController, NotificationController
from ui.resources.styles import (
    STATUS_NEW, STATUS_NEW_BG, STATUS_PROGRESS, STATUS_PROGRESS_BG,
    STATUS_REVIEW, STATUS_REVIEW_BG, STATUS_DONE, STATUS_DONE_BG,
    PRIMARY_COLOR, PRIMARY_LIGHT, TEXT_PRIMARY, TEXT_SECONDARY,
    BG_MAIN, BG_CARD, BORDER, BORDER_LIGHT, ACCENT
)


class KanbanCard(QFrame):
    """Карточка задачи в стиле Bitrix24"""
    def __init__(self, task, status_color, parent=None):
        super().__init__(parent)
        self.task = task
        self.setObjectName("kanban_card")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(90)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 18))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # Верхняя строка: проект
        project_name = getattr(task, 'project_name', 'Проект')
        project_lbl = QLabel(f"📁 {project_name}")
        project_lbl.setObjectName("card_project")
        layout.addWidget(project_lbl)

        # Описание задачи
        desc = task.description if len(task.description) <= 80 else task.description[:77] + '...'
        title_lbl = QLabel(desc)
        title_lbl.setObjectName("card_title")
        title_lbl.setWordWrap(True)
        layout.addWidget(title_lbl)

        # Нижняя строка: разработчик + часы
        bottom = QHBoxLayout()
        bottom.setSpacing(8)

        dev_name = getattr(task, 'developer_name', 'Не назначен')
        dev_lbl = QLabel(f"👤 {dev_name}")
        dev_lbl.setObjectName("card_developer")
        bottom.addWidget(dev_lbl)

        bottom.addStretch()

        hours = getattr(task, 'hours_worked', 0) or 0
        hours_lbl = QLabel(f"⏱ {hours}ч")
        hours_lbl.setObjectName("card_hours")
        bottom.addWidget(hours_lbl)

        layout.addLayout(bottom)

        # Дата
        date_val = getattr(task, 'updated_at', '') or getattr(task, 'created_at', '')
        if date_val:
            date_short = str(date_val)[:10]
            date_lbl = QLabel(date_short)
            date_lbl.setObjectName("card_date")
            layout.addWidget(date_lbl)


class KanbanColumn(QFrame):
    """Колонка Kanban-доски в стиле Bitrix24"""
    def __init__(self, title, tasks_list, color, bg_color, object_suffix, parent=None):
        super().__init__(parent)
        self.setObjectName(f"kanban_column_{object_suffix}")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(10)

        # ─── Header колонки ───
        header = QHBoxLayout()
        header.setSpacing(8)

        color_bar = QFrame()
        color_bar.setFixedSize(4, 22)
        color_bar.setStyleSheet(f"background-color: {color}; border-radius: 2px;")
        header.addWidget(color_bar)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("kanban_col_title")
        header.addWidget(title_lbl)

        header.addStretch()

        count_lbl = QLabel(str(len(tasks_list)))
        count_lbl.setObjectName(f"kanban_col_count_{object_suffix}")
        count_lbl.setAlignment(Qt.AlignCenter)
        count_lbl.setFixedHeight(22)
        header.addWidget(count_lbl)

        layout.addLayout(header)

        # Разделитель
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"background-color: {color}; max-height: 2px; border: none; border-radius: 1px;")
        sep.setFixedHeight(2)
        layout.addWidget(sep)

        # ─── Скролл с карточками ───
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")

        cards_widget = QWidget()
        cards_widget.setStyleSheet("background: transparent;")
        cards_layout = QVBoxLayout(cards_widget)
        cards_layout.setContentsMargins(0, 4, 0, 4)
        cards_layout.setSpacing(10)

        for task in tasks_list:
            card = KanbanCard(task, color)
            cards_layout.addWidget(card)

        add_btn = QPushButton("+ Добавить задачу")
        add_btn.setObjectName("kanban_add")
        add_btn.setFixedHeight(42)
        cards_layout.addWidget(add_btn)

        cards_layout.addStretch()
        scroll.setWidget(cards_widget)
        layout.addWidget(scroll)


class StatCard(QFrame):
    """Карточка статистики в стиле Bitrix24"""
    def __init__(self, title, value, color, icon_text="", subtitle="", parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card")
        self.setFixedHeight(120)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 14))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(16)

        icon_frame = QFrame()
        icon_frame.setFixedSize(52, 52)
        icon_frame.setStyleSheet(f"""
            background-color: {color}18;
            border-radius: 26px;
            border: 2px solid {color}40;
        """)
        icon_lbl = QLabel(icon_text)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setFont(QFont('Segoe UI Emoji', 20))
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(icon_lbl)
        layout.addWidget(icon_frame)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        val_lbl = QLabel(str(value))
        val_lbl.setObjectName("stat_value")
        val_lbl.setStyleSheet(f"color: {color};")
        text_layout.addWidget(val_lbl)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("stat_title")
        text_layout.addWidget(title_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setObjectName("stat_subtitle")
            text_layout.addWidget(sub_lbl)

        layout.addLayout(text_layout)
        layout.addStretch()


class DashboardTab(QWidget):
    """Вкладка Дашборд — Kanban-доска в стиле Bitrix24"""

    KANBAN_STATUSES = [
        {'key': 'новая',       'title': 'Новые',       'color': STATUS_NEW,      'bg': STATUS_NEW_BG,      'suffix': 'new'},
        {'key': 'в работе',    'title': 'В работе',    'color': STATUS_PROGRESS, 'bg': STATUS_PROGRESS_BG, 'suffix': 'progress'},
        {'key': 'на проверке', 'title': 'На проверке', 'color': STATUS_REVIEW,   'bg': STATUS_REVIEW_BG,   'suffix': 'review'},
        {'key': 'завершено',   'title': 'Завершено',   'color': STATUS_DONE,     'bg': STATUS_DONE_BG,     'suffix': 'done'},
    ]

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.project_controller = ProjectController()
        self.task_controller = TaskController()
        self.developer_controller = DeveloperController()
        self.notification_controller = NotificationController()
        self.init_ui()

    def _load_tasks(self):
        if self.user.role == 'developer':
            dev_result = self.developer_controller.get_developer_by_user_id(self.user.id)
            if dev_result.get('success') and dev_result.get('data'):
                tasks_result = self.task_controller.get_tasks_by_developer(dev_result['data'].id)
            else:
                tasks_result = {'success': True, 'data': []}
        else:
            tasks_result = self.task_controller.get_all_tasks()
        return tasks_result.get('data', []) if tasks_result.get('success') else []

    def _load_projects(self):
        if self.user.role == 'developer':
            dev_result = self.developer_controller.get_developer_by_user_id(self.user.id)
            if dev_result.get('success') and dev_result.get('data'):
                return self.project_controller.get_projects_by_developer(dev_result['data'].id)
            return {'success': True, 'data': []}
        return self.project_controller.get_all_projects()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ═══════════ HEADER ═══════════
        header = QFrame()
        header.setStyleSheet(f"background-color: {BG_CARD}; border-bottom: 1px solid {BORDER};")
        header.setFixedHeight(64)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)

        greeting = QLabel(f"👋 {self.user.full_name}")
        greeting.setFont(QFont('Segoe UI', 16, QFont.DemiBold))
        greeting.setStyleSheet(f"color: {TEXT_PRIMARY}; border: none;")
        header_layout.addWidget(greeting)

        header_layout.addStretch()

        refresh_btn = QPushButton("⟳  Обновить")
        refresh_btn.setObjectName("flat")
        refresh_btn.setFixedHeight(36)
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)

        main_layout.addWidget(header)

        # ═══════════ CONTENT ═══════════
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet(f"QScrollArea {{ background-color: {BG_MAIN}; border: none; }}")

        content = QWidget()
        content.setStyleSheet(f"background-color: {BG_MAIN};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(20)

        content_layout.addLayout(self._build_stats_row())

        board_header = QHBoxLayout()
        board_title = QLabel("📋  Kanban-доска")
        board_title.setFont(QFont('Segoe UI', 15, QFont.DemiBold))
        board_title.setStyleSheet(f"color: {TEXT_PRIMARY};")
        board_header.addWidget(board_title)
        board_header.addStretch()
        content_layout.addLayout(board_header)

        content_layout.addWidget(self._build_kanban_board(), stretch=1)

        if self.user.role != 'developer':
            content_layout.addWidget(self.create_notifications_widget())

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area, stretch=1)

    def _build_stats_row(self):
        row = QHBoxLayout()
        row.setSpacing(16)

        all_tasks = self._load_tasks()
        projects_result = self._load_projects()
        projects = projects_result.get('data', []) if projects_result.get('success') else []

        new_count = len([t for t in all_tasks if getattr(t, 'status', '') == 'новая'])
        progress_count = len([t for t in all_tasks if getattr(t, 'status', '') == 'в работе'])
        done_count = len([t for t in all_tasks if getattr(t, 'status', '') == 'завершено'])

        row.addWidget(StatCard("Проекты", len(projects), PRIMARY_COLOR, "📁", "Всего активных"))
        row.addWidget(StatCard("Всего задач", len(all_tasks), "#6C5CE7", "📝", f"Новых: {new_count}"))
        row.addWidget(StatCard("В работе", progress_count, STATUS_PROGRESS, "🔥", "Активные задачи"))
        row.addWidget(StatCard("Завершено", done_count, STATUS_DONE, "✅", "Выполненных"))

        return row

    def _build_kanban_board(self):
        board_frame = QFrame()
        board_frame.setStyleSheet("background: transparent; border: none;")

        board_layout = QHBoxLayout(board_frame)
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(14)

        all_tasks = self._load_tasks()

        for status_info in self.KANBAN_STATUSES:
            filtered = [t for t in all_tasks if getattr(t, 'status', '').lower() == status_info['key']]
            column = KanbanColumn(
                title=status_info['title'],
                tasks_list=filtered,
                color=status_info['color'],
                bg_color=status_info['bg'],
                object_suffix=status_info['suffix']
            )
            board_layout.addWidget(column)

        return board_frame

    def show_all_tasks(self):
        window = self.window()
        if hasattr(window, '_switch_to_key'):
            window._switch_to_key('tasks')

    def refresh_data(self):
        try:
            self.notification_controller.run_all_checks()
            self.project_controller = ProjectController()
            self.task_controller = TaskController()
            self.developer_controller = DeveloperController()
            self.notification_controller = NotificationController()

            layout = self.layout()
            if layout:
                while layout.count():
                    item = layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                self.init_ui()
        except Exception as e:
            import traceback
            print(f"Ошибка при обновлении дашборда: {str(e)}")
            print(traceback.format_exc())

    def create_notifications_widget(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFrameShadow(QFrame.Raised)
        frame.setObjectName('notifications_panel')

        layout = QVBoxLayout(frame)

        header_layout = QHBoxLayout()
        title_label = QLabel("Уведомления")
        title_label.setFont(QFont('Segoe UI', 14, QFont.Bold))
        header_layout.addWidget(title_label)

        mark_all_button = QPushButton("Отметить все как прочитанные")
        mark_all_button.setObjectName("flat")
        mark_all_button.clicked.connect(self.mark_all_notifications_as_read)
        header_layout.addWidget(mark_all_button, alignment=Qt.AlignRight)
        layout.addLayout(header_layout)

        try:
            notifications_result = self.notification_controller.get_all_notifications(limit=5, only_unread=True)
            notifications = notifications_result.get('data', []) if isinstance(notifications_result, dict) else []

            if notifications:
                for notification in notifications:
                    layout.addWidget(self.create_notification_item(notification))
            else:
                no_lbl = QLabel("Нет новых уведомлений")
                no_lbl.setAlignment(Qt.AlignCenter)
                layout.addWidget(no_lbl)
        except Exception as e:
            error_label = QLabel(f"Ошибка загрузки уведомлений: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setStyleSheet("color: red;")
            layout.addWidget(error_label)

        return frame

    def create_notification_item(self, notification):
        item = QFrame()
        item.setObjectName(f"notification_{notification.type}")
        item.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(10, 10, 10, 10)

        icon_path = {
            'info': 'ui/resources/icons/info.png',
            'success': 'ui/resources/icons/success.png',
            'warning': 'ui/resources/icons/warning.png',
            'error': 'ui/resources/icons/error.png'
        }.get(notification.type, 'ui/resources/icons/info.png')

        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(24, 24)))
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        title_label = QLabel(notification.title)
        title_label.setObjectName("notification_text")
        title_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        message_label = QLabel(notification.message)
        text_layout.addWidget(title_label)
        text_layout.addWidget(message_label)
        layout.addLayout(text_layout)
        layout.addStretch()

        close_button = QPushButton("×")
        close_button.setObjectName("notification_close")
        close_button.setFixedSize(24, 24)
        close_button.clicked.connect(lambda: self.mark_notification_as_read(notification.id))
        layout.addWidget(close_button, alignment=Qt.AlignTop)

        return item

    def mark_all_notifications_as_read(self):
        result = self.notification_controller.mark_all_as_read()
        if result['success']:
            self.refresh_data()

    def mark_notification_as_read(self, notification_id):
        result = self.notification_controller.mark_as_read(notification_id)
        if result['success']:
            self.refresh_data()
