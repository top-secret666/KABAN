from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QPushButton, QButtonGroup, QSizePolicy,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from ui.resources.styles import SIDEBAR_TEXT_DIM, TEXT_WHITE


class SidebarButton(QPushButton):
    def __init__(self, text, icon_char='', parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_char}  {text}" if icon_char else f"  {text}")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(44)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFont(QFont('Segoe UI', 10))


class Sidebar(QFrame):
    """Левая панель навигации в стиле Bitrix24."""

    navigated = pyqtSignal(int)

    _ALL_ITEMS = [
        ('dashboard', '📊', 'Дашборд'),
        ('developers', '👥', 'Разработчики'),
        ('projects', '📁', 'Проекты'),
        ('tasks', '✅', 'Задачи'),
        ('reports', '📈', 'Отчёты'),
        ('settings', '⚙', 'Настройки'),
        ('admin', '🔐', 'Администрирование'),
    ]

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._buttons = []
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._items = self._build_item_list()
        self.setObjectName('sidebar')
        self.setFixedWidth(240)
        self._build()

    def _build_item_list(self):
        role = self.user.role
        items = [('dashboard', '📊', 'Дашборд'), ('projects', '📁', 'Проекты'), ('tasks', '✅', 'Задачи')]
        if role != 'developer':
            items = [
                ('dashboard', '📊', 'Дашборд'),
                ('developers', '👥', 'Разработчики'),
                ('projects', '📁', 'Проекты'),
                ('tasks', '✅', 'Задачи'),
                ('reports', '📈', 'Отчёты'),
                ('settings', '⚙', 'Настройки'),
            ]
        if role == 'admin':
            items.append(('admin', '🔐', 'Администрирование'))
        return items

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo_frame = QFrame()
        logo_frame.setObjectName('sidebar_logo')
        logo_frame.setFixedHeight(64)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(20, 14, 16, 14)

        title = QLabel('KABAN')
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setStyleSheet(f'color: {TEXT_WHITE}; background: transparent; border: none;')

        subtitle = QLabel('manager')
        subtitle.setFont(QFont('Segoe UI', 9))
        subtitle.setStyleSheet(f'color: {SIDEBAR_TEXT_DIM}; background: transparent; border: none;')

        self._logo_title = title
        self._logo_subtitle = subtitle

        logo_layout.addWidget(title)
        logo_layout.addWidget(subtitle)
        layout.addWidget(logo_frame)

        nav_frame = QFrame()
        nav_frame.setObjectName('sidebar_nav')
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(8, 12, 8, 12)
        nav_layout.setSpacing(2)

        for stack_idx, (key, icon, label) in enumerate(self._items):
            btn = SidebarButton(label, icon)
            btn.setObjectName('sidebar_btn')
            btn.clicked.connect(lambda checked, i=stack_idx: self._on_click(i))
            self._group.addButton(btn)
            self._buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        layout.addWidget(nav_frame, stretch=1)

        user_frame = QFrame()
        user_frame.setObjectName('sidebar_user')
        user_frame.setFixedHeight(68)
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(20, 10, 16, 10)
        user_layout.setSpacing(2)

        role_map = {'admin': 'Администратор', 'manager': 'Менеджер', 'developer': 'Разработчик'}
        name_lbl = QLabel(self.user.full_name)
        name_lbl.setFont(QFont('Segoe UI', 10, QFont.DemiBold))
        name_lbl.setStyleSheet(f'color: {TEXT_WHITE}; background: transparent; border: none;')

        role_lbl = QLabel(role_map.get(self.user.role, self.user.role))
        role_lbl.setFont(QFont('Segoe UI', 9))
        role_lbl.setStyleSheet(f'color: {SIDEBAR_TEXT_DIM}; background: transparent; border: none;')

        self._user_name = name_lbl
        self._user_role = role_lbl

        user_layout.addWidget(name_lbl)
        user_layout.addWidget(role_lbl)
        layout.addWidget(user_frame)

        if self._buttons:
            self._buttons[0].setChecked(True)

    def _on_click(self, stack_index):
        self.navigated.emit(stack_index)

    def set_active_index(self, stack_index):
        for i, btn in enumerate(self._buttons):
            btn.setChecked(i == stack_index)

    def item_keys(self):
        return [item[0] for item in self._items]

    def refresh_theme(self):
        from ui.resources.styles import TEXT_WHITE, SIDEBAR_TEXT_DIM
        for lbl, color in (
            (getattr(self, '_logo_title', None), TEXT_WHITE),
            (getattr(self, '_user_name', None), TEXT_WHITE),
            (getattr(self, '_logo_subtitle', None), SIDEBAR_TEXT_DIM),
            (getattr(self, '_user_role', None), SIDEBAR_TEXT_DIM),
        ):
            if lbl:
                lbl.setStyleSheet(
                    f'color: {color}; background: transparent; border: none;'
                )
