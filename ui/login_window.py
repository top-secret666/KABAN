import os
import sys
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QMessageBox, QApplication, QFrame,
                             QGraphicsDropShadowEffect)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QSize

from ui.resources.theme_manager import get_login_styles, get_config
from controllers import AuthController


class LoginWindow(QDialog):
    """Окно входа в систему — Bitrix24 стиль"""

    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('KABAN:manager')
        self.setWindowIcon(QIcon('ui/resources/icons/logo.png'))
        self.setFixedSize(440, 560)
        self.setWindowFlags(
            Qt.Dialog | Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint
        )

        ls = get_login_styles(get_config())

        self.setStyleSheet(f"""
            QDialog {{
                background: {ls['gradient']};
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setAlignment(Qt.AlignCenter)

        # ─── Белая карточка ───
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {ls['card_bg']};
                border-radius: 16px;
                border: none;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 36, 32, 32)
        card_layout.setSpacing(12)

        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap('ui/resources/icons/logo.png')
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("border: none; background: transparent;")
        card_layout.addWidget(logo_label)

        # Заголовок
        title = QLabel('KABAN:manager')
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {ls['text_primary']}; border: none; background: transparent;")
        card_layout.addWidget(title)

        subtitle = QLabel('Войдите в свой аккаунт')
        subtitle.setFont(QFont('Segoe UI', 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {ls['text_secondary']}; border: none; margin-bottom: 8px; background: transparent;")
        card_layout.addWidget(subtitle)

        # Поля ввода
        input_style = f"""
            QLineEdit {{
                border: 2px solid {BORDER};
                border-radius: 10px;
                padding: 12px 16px;
                font-size: 14px;
                font-family: 'Segoe UI';
                background-color: #F8F9FB;
                color: {TEXT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY_COLOR};
                background-color: {BG_CARD};
            }}
            QLineEdit::placeholder {{
                color: {TEXT_SECONDARY};
            }}
        """

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('👤  Имя пользователя')
        self.username_input.setMinimumHeight(48)
        self.username_input.setStyleSheet(input_style)
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('🔒  Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(48)
        self.password_input.setStyleSheet(input_style)
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(8)

        # Кнопка входа
        self.login_button = QPushButton('Войти')
        self.login_button.setMinimumHeight(48)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setFont(QFont('Segoe UI', 13, QFont.Bold))
        self.login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_DARK};
            }}
            QPushButton:pressed {{
                background-color: #1838A0;
            }}
        """)
        self.login_button.clicked.connect(self.login)
        card_layout.addWidget(self.login_button)

        # Кнопка регистрации
        self.register_button = QPushButton('Нет аккаунта? Регистрация')
        self.register_button.setMinimumHeight(40)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setFont(QFont('Segoe UI', 11))
        self.register_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {PRIMARY_COLOR};
                border: none;
                font-weight: 600;
            }}
            QPushButton:hover {{
                color: {PRIMARY_DARK};
                text-decoration: underline;
            }}
        """)
        self.register_button.clicked.connect(self.show_register)
        card_layout.addWidget(self.register_button)

        # Версия
        version = QLabel('v1.0.0')
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 10px; border: none; background: transparent;")
        card_layout.addWidget(version)

        main_layout.addWidget(card)

        # Фокус и Enter
        self.username_input.setFocus()
        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

    def login(self):
        """
        Обработка входа в систему
        """
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите имя пользователя и пароль')
            return

        # Попытка входа
        result = self.auth_controller.login(username, password)

        if result['success']:
            self.user = result['data']
            QMessageBox.information(self, 'Успех', f'Добро пожаловать, {self.user.full_name}!')
            self.accept()  # вызовет super().accept()
        else:
            QMessageBox.critical(self, 'Ошибка', result['error_message'])

    def show_register(self):
        """
        Показать окно регистрации
        """
        from ui.register_window import RegisterWindow
        register_window = RegisterWindow()
        if register_window.exec_():
            # Если регистрация успешна, заполняем поля для входа
            self.username_input.setText(register_window.username)
            self.password_input.setText(register_window.password)

    def accept(self):
        super().accept()

    def closeEvent(self, event):
        """
        Обработка закрытия окна
        """
        if not hasattr(self, 'accepted') or not self.accepted:
            reply = QMessageBox.question(
                self, 'Выход', 'Вы уверены, что хотите выйти?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                event.accept()
                sys.exit(0)
            else:
                event.ignore()
