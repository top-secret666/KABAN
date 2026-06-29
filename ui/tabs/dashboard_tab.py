from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFrame, QScrollArea, QSizePolicy, QGridLayout, QTabWidget,
                             QGraphicsDropShadowEffect, QSpacerItem, QMessageBox)
from PyQt5.QtGui import QFont, QIcon, QColor, QPainter, QPainterPath, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from controllers import ProjectController, TaskController, DeveloperController, NotificationController
from ui.dialogs.task_dialog import TaskDialog
from ui.resources.icon_helper import get_icon
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
    def __init__(self, title, tasks_list, color, bg_color, object_suffix,
                 on_add_task=None, parent=None):
        super().__init__(parent)
        self._on_add_task = on_add_task
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
        add_btn.setCursor(Qt.PointingHandCursor)
        if self._on_add_task:
            add_btn.clicked.connect(self._on_add_task)
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
        if hasattr(self, '_content_layout'):
            self._reload_dashboard()
            return

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QFrame()
        header.setObjectName('dashboard_header')
        header.setStyleSheet(
            f"QFrame#dashboard_header {{"
            f" background-color: {BG_CARD}; border-bottom: 1px solid {BORDER}; }}"
        )
        header.setFixedHeight(64)
        self._header = header
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 0, 24, 0)

        greeting = QLabel(f"👋 {self.user.full_name}")
        greeting.setObjectName('dashboard_greeting')
        greeting.setFont(QFont('Segoe UI', 16, QFont.DemiBold))
        greeting.setStyleSheet(
            f"QLabel#dashboard_greeting {{ color: {TEXT_PRIMARY}; border: none; background: transparent; }}"
        )
        self._greeting = greeting
        header_layout.addWidget(greeting)
        header_layout.addStretch()

        refresh_btn = QPushButton("⟳  Обновить")
        refresh_btn.setObjectName("flat")
        refresh_btn.setFixedHeight(36)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        main_layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet(f"QScrollArea {{ background-color: {BG_MAIN}; border: none; }}")
        self._scroll_area = scroll_area

        content = QWidget()
        content.setObjectName('dashboard_content')
        content.setStyleSheet(
            f"QWidget#dashboard_content {{ background-color: {BG_MAIN}; }}"
        )
        self._content = content
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(24, 20, 24, 20)
        self._content_layout.setSpacing(20)

        self._stats_host = QWidget()
        self._stats_host.setObjectName('dashboard_stats')
        self._stats_host.setStyleSheet(
            "QWidget#dashboard_stats { background: transparent; border: none; }"
        )
        self._stats_layout = QHBoxLayout(self._stats_host)
        self._stats_layout.setContentsMargins(0, 0, 0, 0)
        self._stats_layout.setSpacing(16)
        self._content_layout.addWidget(self._stats_host)

        board_header = QHBoxLayout()
        board_title = QLabel("📋  Kanban-доска")
        board_title.setObjectName('dashboard_board_title')
        board_title.setFont(QFont('Segoe UI', 15, QFont.DemiBold))
        board_title.setStyleSheet(
            f"QLabel#dashboard_board_title {{ color: {TEXT_PRIMARY}; background: transparent; border: none; }}"
        )
        self._board_title = board_title
        board_header.addWidget(board_title)
        board_header.addStretch()

        add_task_btn = QPushButton("  Новая задача")
        add_task_btn.setObjectName("btn_primary")
        add_task_btn.setFixedHeight(36)
        add_task_btn.setMinimumWidth(140)
        add_task_btn.setCursor(Qt.PointingHandCursor)
        add_task_btn.setIcon(get_icon('add'))
        add_task_btn.clicked.connect(lambda: self.add_task('новая'))
        self._add_task_btn = add_task_btn
        board_header.addWidget(add_task_btn)
        self._apply_add_task_btn_style()
        self._content_layout.addLayout(board_header)

        self._kanban_host = QFrame()
        self._kanban_host.setObjectName('dashboard_kanban')
        self._kanban_host.setStyleSheet(
            "QFrame#dashboard_kanban { background: transparent; border: none; }"
        )
        self._kanban_layout = QHBoxLayout(self._kanban_host)
        self._kanban_layout.setContentsMargins(0, 0, 0, 0)
        self._kanban_layout.setSpacing(14)
        self._content_layout.addWidget(self._kanban_host, stretch=1)

        if self.user.role != 'developer':
            self._notifications_host = QFrame()
            self._notifications_host.setFrameShape(QFrame.NoFrame)
            self._notifications_host.setObjectName('notifications_panel')
            self._notifications_layout = QVBoxLayout(self._notifications_host)
            self._notifications_layout.setContentsMargins(20, 16, 20, 16)
            self._notifications_layout.setSpacing(12)
            self._content_layout.addWidget(self._notifications_host)
        else:
            self._notifications_host = None
            self._notifications_layout = None

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area, stretch=1)

        self._reload_dashboard()

    def _clear_layout(self, layout):
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            sub = item.layout()
            if sub:
                self._clear_layout(sub)

    def _reload_dashboard(self):
        self._clear_layout(self._stats_layout)
        for card in self._build_stat_cards():
            self._stats_layout.addWidget(card)

        self._clear_layout(self._kanban_layout)
        all_tasks = self._load_tasks()
        for status_info in self.KANBAN_STATUSES:
            filtered = [
                t for t in all_tasks
                if getattr(t, 'status', '').lower() == status_info['key']
            ]
            status_key = status_info['key']
            column = KanbanColumn(
                title=status_info['title'],
                tasks_list=filtered,
                color=status_info['color'],
                bg_color=status_info['bg'],
                object_suffix=status_info['suffix'],
                on_add_task=lambda checked=False, s=status_key: self.add_task(s),
            )
            self._kanban_layout.addWidget(column)

        if self._notifications_layout is not None:
            self._clear_layout(self._notifications_layout)
            self._populate_notifications(self._notifications_layout)

    def _build_stat_cards(self):
        all_tasks = self._load_tasks()
        projects_result = self._load_projects()
        projects = projects_result.get('data', []) if projects_result.get('success') else []

        new_count = len([t for t in all_tasks if getattr(t, 'status', '') == 'новая'])
        progress_count = len([t for t in all_tasks if getattr(t, 'status', '') == 'в работе'])
        done_count = len([t for t in all_tasks if getattr(t, 'status', '') == 'завершено'])

        return [
            StatCard("Проекты", len(projects), PRIMARY_COLOR, "📁", "Всего активных"),
            StatCard("Всего задач", len(all_tasks), "#6C5CE7", "📝", f"Новых: {new_count}"),
            StatCard("В работе", progress_count, STATUS_PROGRESS, "🔥", "Активные задачи"),
            StatCard("Завершено", done_count, STATUS_DONE, "✅", "Выполненных"),
        ]

    def _populate_notifications(self, layout):
        header_layout = QHBoxLayout()
        title_label = QLabel("🔔  Уведомления")
        title_label.setFont(QFont('Segoe UI', 14, QFont.DemiBold))
        title_label.setStyleSheet(f"color: {TEXT_PRIMARY}; border: none;")
        header_layout.addWidget(title_label)

        mark_all_button = QPushButton("Отметить все как прочитанные")
        mark_all_button.setObjectName("flat")
        mark_all_button.clicked.connect(self.mark_all_notifications_as_read)
        header_layout.addWidget(mark_all_button, alignment=Qt.AlignRight)
        layout.addLayout(header_layout)

        try:
            notifications_result = self.notification_controller.get_all_notifications(
                limit=5, only_unread=True
            )
            notifications = (
                notifications_result.get('data', [])
                if isinstance(notifications_result, dict) else []
            )
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

    def add_task(self, default_status='новая'):
        default_developer_id = None
        if self.user.role == 'developer':
            dev_result = self.developer_controller.get_developer_by_user_id(self.user.id)
            if dev_result.get('success') and dev_result.get('data'):
                default_developer_id = dev_result['data'].id

        dialog = TaskDialog(
            self,
            default_status=default_status,
            default_developer_id=default_developer_id,
        )
        if dialog.exec_():
            task_data = {
                'project_id': dialog.project_combo.currentData(),
                'developer_id': dialog.developer_combo.currentData(),
                'description': dialog.description_input.toPlainText(),
                'status': dialog.status_combo.currentText(),
                'hours_worked': float(dialog.hours_input.text() or 0),
            }
            result = self.task_controller.create_task(task_data)
            if result['success']:
                QMessageBox.information(self, "Успех", "Задача успешно добавлена")
                self._reload_dashboard()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])

    def _apply_add_task_btn_style(self):
        from ui.resources.theme_manager import current_palette
        p = current_palette()
        self._add_task_btn.setStyleSheet(f"""
            QPushButton#btn_primary {{
                background-color: {p['primary']};
                color: {p['text_on_primary']};
                border: 1px solid {p['primary_dark']};
                border-radius: 8px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton#btn_primary:hover {{
                background-color: {p['primary_dark']};
                border-color: {p['primary_pressed']};
            }}
        """)

    def show_all_tasks(self):
        window = self.window()
        if hasattr(window, '_switch_to_key'):
            window._switch_to_key('tasks')

    def refresh_theme(self):
        from ui.resources import styles as s
        if hasattr(self, '_header'):
            self._header.setStyleSheet(
                f"QFrame#dashboard_header {{"
                f" background-color: {s.BG_CARD}; border-bottom: 1px solid {s.BORDER}; }}"
            )
        if hasattr(self, '_greeting'):
            self._greeting.setStyleSheet(
                f"QLabel#dashboard_greeting {{ color: {s.TEXT_PRIMARY}; border: none; background: transparent; }}"
            )
        if hasattr(self, '_scroll_area'):
            self._scroll_area.setStyleSheet(
                f"QScrollArea {{ background-color: {s.BG_MAIN}; border: none; }}"
            )
        if hasattr(self, '_content'):
            self._content.setStyleSheet(
                f"QWidget#dashboard_content {{ background-color: {s.BG_MAIN}; }}"
            )
        if hasattr(self, '_board_title'):
            self._board_title.setStyleSheet(
                f"QLabel#dashboard_board_title {{ color: {s.TEXT_PRIMARY}; background: transparent; border: none; }}"
            )
        if hasattr(self, '_add_task_btn'):
            self._apply_add_task_btn_style()

    def refresh_data(self):
        try:
            self.notification_controller.run_all_checks()
            self.project_controller = ProjectController()
            self.task_controller = TaskController()
            self.developer_controller = DeveloperController()
            self.notification_controller = NotificationController()
            self._reload_dashboard()
        except Exception:
            pass

    def create_notifications_widget(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setObjectName('notifications_panel')
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        self._populate_notifications(layout)
        return frame

    def create_notification_item(self, notification):
        item = QFrame()
        item.setObjectName(f"notification_{notification.type}")
        item.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(item)
        layout.setContentsMargins(10, 10, 10, 10)

        icon_label = QLabel()
        icon_label.setPixmap(get_icon(notification.type).pixmap(QSize(24, 24)))
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
            self._reload_dashboard()

    def mark_notification_as_read(self, notification_id):
        result = self.notification_controller.mark_as_read(notification_id)
        if result['success']:
            self._reload_dashboard()
