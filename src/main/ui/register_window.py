from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFormLayout, QMessageBox, QComboBox, QFrame)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from .resources.styles import GLOBAL_STYLE
from src.main.security import AuthController

class RegisterWindow(QDialog):
    """
    Окно регистрации нового пользователя
    """
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.username = ""
        self.password = ""
        self.init_ui()
        self.setStyleSheet(GLOBAL_STYLE)
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('KABAN:manager - Регистрация')
        self.setWindowIcon(QIcon('src/main/ui/resources/icons/kaban.png'))
        self.setFixedSize(450, 500)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        
        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Заголовок
        title_label = QLabel('Регистрация нового пользователя')
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Форма регистрации
        register_frame = QFrame()
        register_frame.setFrameShape(QFrame.StyledPanel)
        register_frame.setFrameShadow(QFrame.Raised)
        register_layout = QFormLayout()
        register_layout.setContentsMargins(20, 20, 20, 20)
        register_layout.setSpacing(15)
        
        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите имя пользователя')
        self.username_input.setMinimumHeight(40)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Подтвердите пароль')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumHeight(40)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Введите email')
        self.email_input.setMinimumHeight(40)
        
        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText('Введите полное имя')
        self.full_name_input.setMinimumHeight(40)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(['developer', 'manager', 'admin'])
        self.role_combo.setMinimumHeight(40)
        
        register_layout.addRow('Имя пользователя*:', self.username_input)
        register_layout.addRow('Пароль*:', self.password_input)
        register_layout.addRow('Подтверждение пароля*:', self.confirm_password_input)
        register_layout.addRow('Email*:', self.email_input)
        register_layout.addRow('Полное имя*:', self.full_name_input)
        register_layout.addRow('Роль*:', self.role_combo)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.register_button = QPushButton('Зарегистрироваться')
        self.register_button.setMinimumHeight(40)
        self.register_button.clicked.connect(self.register)
        
        self.cancel_button = QPushButton('Отмена')
        self.cancel_button.setObjectName('flat')
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.register_button)
        buttons_layout.addWidget(self.cancel_button)
        
        register_layout.addRow('', buttons_layout)
        register_frame.setLayout(register_layout)
        main_layout.addWidget(register_frame)
        
        # Примечание
        note_label = QLabel('* - обязательные поля')
        note_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(note_label)
        
        self.setLayout(main_layout)
        
        # Фокус на поле имени пользователя
        self.username_input.setFocus()
    
    def register(self):
        """
        Обработка регистрации
        """
        # Получение данных из полей
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.email_input.text().strip()
        full_name = self.full_name_input.text().strip()
        role = self.role_combo.currentText()
        
        # Проверка заполнения обязательных полей
        if not username or not password or not confirm_password or not email or not full_name:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все обязательные поля')
            return
        
        # Проверка совпадения паролей
        if password != confirm_password:
            QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают')
            return
        
        # Проверка формата email (простая проверка)
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите корректный email')
            return
        
        # Попытка регистрации
        result = self.auth_controller.register(username, password, email, full_name, role)
        
        if result['success']:
            QMessageBox.information(self, 'Успех', 'Регистрация успешно завершена!')
            self.username = username
            self.password = password
            self.accept()
        else:
            QMessageBox.critical(self, 'Ошибка', result['error_message'])
