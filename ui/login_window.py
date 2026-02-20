import os
import sys
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QMessageBox, QApplication, QFrame)
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from ui.resources.styles import GLOBAL_STYLE
from controllers import AuthController


class LoginWindow(QDialog):
    """
    Окно входа в систему
    """

    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.init_ui()
        self.setStyleSheet(GLOBAL_STYLE)

    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('KABAN:manager - Вход в систему')
        self.setWindowIcon(QIcon('ui/resources/icons/logo.png'))
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Логотип
        logo_layout = QHBoxLayout()
        logo_label = QLabel()
        logo_pixmap = QPixmap('ui/resources/icons/logo.png')
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        main_layout.addLayout(logo_layout)

        # Заголовок
        title_label = QLabel('KABAN:manager')
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Форма входа
        login_frame = QFrame()
        login_frame.setFrameShape(QFrame.StyledPanel)
        login_frame.setFrameShadow(QFrame.Raised)
        login_layout = QFormLayout()
        login_layout.setContentsMargins(20, 20, 20, 20)
        login_layout.setSpacing(15)

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Имя пользователя')
        self.username_input.setMinimumHeight(40)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)

        login_layout.addRow('Имя пользователя:', self.username_input)
        login_layout.addRow('Пароль:', self.password_input)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.login_button = QPushButton('Войти')
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton('Регистрация')
        self.register_button.setObjectName('flat')
        self.register_button.setMinimumHeight(40)
        self.register_button.clicked.connect(self.show_register)

        buttons_layout.addWidget(self.login_button)
        buttons_layout.addWidget(self.register_button)

        login_layout.addRow('', buttons_layout)
        login_frame.setLayout(login_layout)
        main_layout.addWidget(login_frame)

        # Информация о версии
        version_label = QLabel('Версия 1.0.0')
        version_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(version_label)

        self.setLayout(main_layout)

        # Фокус на поле имени пользователя
        self.username_input.setFocus()

        # Подключение Enter к кнопке входа
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
