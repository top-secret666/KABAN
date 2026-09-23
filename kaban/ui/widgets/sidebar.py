from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QSizePolicy,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from ui.resources.styles import SIDEBAR_TEXT_DIM, TEXT_WHITE, PRIMARY_COLOR


class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(f"  {text}")
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFont(QFont('Segoe UI', 10, QFont.Medium))


class Sidebar(QFrame):

    navigated = pyqtSignal(int)

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._buttons = []
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._items = self._build_item_list()
        self.setObjectName('sidebar')
        self.setFixedWidth(248)
        self._build()

    def _build_item_list(self):
        role = self.user.role
        items = [
            ('dashboard', 'Дашборд'),
            ('projects', 'Проекты'),
            ('tasks', 'Задачи'),
        ]
        if role != 'developer':
            items = [
                ('dashboard', 'Дашборд'),
                ('developers', 'Разработчики'),
                ('projects', 'Проекты'),
                ('tasks', 'Задачи'),
                ('reports', 'Отчёты'),
                ('settings', 'Настройки'),
            ]
        if role == 'admin':
            items.append(('admin', 'Администрирование'))
        return items

    def _initials(self):
        parts = (self.user.full_name or '').split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[1][0]).upper()
        name = self.user.full_name or self.user.username or '?'
        return name[:2].upper()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo_frame = QFrame()
        logo_frame.setObjectName('sidebar_logo')
        logo_frame.setFixedHeight(72)
        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(22, 18, 16, 12)
        logo_layout.setSpacing(0)

        title = QLabel('KABAN')
        title.setFont(QFont('Segoe UI', 17, QFont.Bold))
        title.setStyleSheet(f'color: {TEXT_WHITE}; background: transparent; border: none;')

        subtitle = QLabel('manager')
        subtitle.setFont(QFont('Segoe UI', 10))
        subtitle.setStyleSheet(
            f'color: {PRIMARY_COLOR}; background: transparent; border: none; letter-spacing: 1px;'
        )

        self._logo_title = title
        self._logo_subtitle = subtitle

        logo_layout.addWidget(title)
        logo_layout.addWidget(subtitle)
        layout.addWidget(logo_frame)

        nav_frame = QFrame()
        nav_frame.setObjectName('sidebar_nav')
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 8, 0, 12)
        nav_layout.setSpacing(2)

        for stack_idx, (key, label) in enumerate(self._items):
            btn = SidebarButton(label)
            btn.setObjectName('sidebar_btn')
            btn.clicked.connect(lambda checked, i=stack_idx: self._on_click(i))
            self._group.addButton(btn)
            self._buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()
        layout.addWidget(nav_frame, stretch=1)

        user_frame = QFrame()
        user_frame.setObjectName('sidebar_user')
        user_frame.setFixedHeight(72)
        user_row = QHBoxLayout(user_frame)
        user_row.setContentsMargins(18, 12, 16, 12)
        user_row.setSpacing(12)

        avatar = QLabel(self._initials())
        avatar.setObjectName('sidebar_avatar')
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignCenter)
        avatar.setFont(QFont('Segoe UI', 11, QFont.DemiBold))

        text_col = QVBoxLayout()
        text_col.setSpacing(1)

        role_map = {'admin': 'Администратор', 'manager': 'Менеджер', 'developer': 'Разработчик'}
        name_lbl = QLabel(self.user.full_name)
        name_lbl.setFont(QFont('Segoe UI', 10, QFont.DemiBold))
        name_lbl.setStyleSheet(f'color: {TEXT_WHITE}; background: transparent; border: none;')

        role_lbl = QLabel(role_map.get(self.user.role, self.user.role))
        role_lbl.setFont(QFont('Segoe UI', 9))
        role_lbl.setStyleSheet(f'color: {SIDEBAR_TEXT_DIM}; background: transparent; border: none;')

        self._user_name = name_lbl
        self._user_role = role_lbl
        self._avatar = avatar

        text_col.addWidget(name_lbl)
        text_col.addWidget(role_lbl)
        user_row.addWidget(avatar)
        user_row.addLayout(text_col)
        user_row.addStretch()
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

    def item_labels(self):
        return [item[1] for item in self._items]

    def refresh_theme(self):
        from ui.resources.styles import TEXT_WHITE, SIDEBAR_TEXT_DIM, PRIMARY_COLOR
        for lbl, color in (
            (getattr(self, '_logo_title', None), TEXT_WHITE),
            (getattr(self, '_user_name', None), TEXT_WHITE),
            (getattr(self, '_logo_subtitle', None), PRIMARY_COLOR),
            (getattr(self, '_user_role', None), SIDEBAR_TEXT_DIM),
        ):
            if lbl:
                extra = ' letter-spacing: 1px;' if lbl is getattr(self, '_logo_subtitle', None) else ''
                lbl.setStyleSheet(
                    f'color: {color}; background: transparent; border: none;{extra}'
                )
