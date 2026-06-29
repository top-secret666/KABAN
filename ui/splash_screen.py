from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QFrame
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer

from ui.resources.theme_manager import current_palette, get_login_styles, get_config


class SplashScreen(QWidget):
    """Заставка при загрузке в стиле Bitrix24."""

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFixedSize(480, 320)
        self._build()
        self._center()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.loading_messages = [
            'Инициализация приложения...',
            'Подключение к базе данных...',
            'Загрузка компонентов интерфейса...',
            'Проверка уведомлений...',
            'Загрузка настроек...',
            'Подготовка рабочего пространства...',
            'Почти готово...',
        ]

    def _center(self):
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2,
        )

    def _build(self):
        ls = get_login_styles(get_config())
        p = current_palette()

        self.setStyleSheet(f"""
            QWidget {{
                background: {ls['gradient']};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 36)
        layout.setSpacing(12)

        logo = QLabel()
        pix = QPixmap('ui/resources/icons/logo.png')
        if not pix.isNull():
            logo.setPixmap(pix.scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet('background: transparent; border: none;')
        layout.addWidget(logo)

        self.title_label = QLabel('KABAN:manager')
        self.title_label.setFont(QFont('Segoe UI', 22, QFont.Bold))
        self.title_label.setStyleSheet(f'color: {p["text_white"]}; background: transparent; border: none;')
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.status_label = QLabel('Загрузка...')
        self.status_label.setFont(QFont('Segoe UI', 10))
        self.status_label.setStyleSheet('color: rgba(255,255,255,0.85); background: transparent; border: none;')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addSpacing(8)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 2px;
                background-color: rgba(255,255,255,0.25);
            }}
            QProgressBar::chunk {{
                background-color: {p['text_white']};
                border-radius: 2px;
            }}
        """)
        layout.addWidget(self.progress_bar)

        layout.addStretch()

        self.version_label = QLabel('Версия 1.0.0')
        self.version_label.setFont(QFont('Segoe UI', 9))
        self.version_label.setStyleSheet('color: rgba(255,255,255,0.6); background: transparent; border: none;')
        self.version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.version_label)

    def start_progress(self):
        self.timer.start(100)

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        message_index = min(len(self.loading_messages) - 1, self.progress_value // 15)
        self.status_label.setText(self.loading_messages[message_index])
        if self.progress_value >= 100:
            self.timer.stop()

    def show(self):
        super().show()
        self.raise_()
        self.activateWindow()
