from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QMessageBox, QFrame, QGraphicsDropShadowEffect, QScrollArea, QWidget)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QColor
from PyQt5.QtCore import Qt

from ui.resources.styles import (
    PRIMARY_COLOR, PRIMARY_DARK, PRIMARY_LIGHT,
    TEXT_PRIMARY, TEXT_SECONDARY, BG_CARD, BORDER,
)
from controllers import AuthController


class RegisterWindow(QDialog):
    """Окно регистрации — стиль Bitrix24."""

    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.username = ""
        self.password = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('KABAN:manager — Регистрация')
        self.setWindowIcon(QIcon('ui/resources/icons/logo.png'))
        self.setFixedSize(480, 620)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)

        self.setStyleSheet(f"""
            QDialog {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {PRIMARY_COLOR}, stop:0.5 #4AD4F5, stop:1 {PRIMARY_DARK});
            }}
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 32, 32, 32)

        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: {BG_CARD}; border-radius: 12px; border: none; }}")
        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 60))
        card.setGraphicsEffect(shadow)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet('QScrollArea { background: transparent; border: none; }')

        inner = QWidget()
        inner.setStyleSheet('background: transparent;')
        card_layout = QVBoxLayout(inner)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(12)

        title = QLabel('Регистрация')
        title.setFont(QFont('Segoe UI', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {TEXT_PRIMARY}; border: none; background: transparent;")
        card_layout.addWidget(title)

        subtitle = QLabel('Создайте новый аккаунт')
        subtitle.setFont(QFont('Segoe UI', 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"color: {TEXT_SECONDARY}; border: none; margin-bottom: 8px;")
        card_layout.addWidget(subtitle)

        input_style = f"""
            QLineEdit, QComboBox {{
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 10px 14px;
                font-size: 14px;
                font-family: 'Segoe UI';
                background-color: #FAFBFC;
                color: {TEXT_PRIMARY};
                min-height: 20px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border: 1px solid {PRIMARY_COLOR};
                background-color: {BG_CARD};
            }}
        """

        from PyQt5.QtWidgets import QComboBox, QFormLayout
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignLeft)

        label_style = f"color: {TEXT_SECONDARY}; font-size: 12px; border: none;"

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Имя пользователя')
        self.username_input.setStyleSheet(input_style)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Подтвердите пароль')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(input_style)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('email@example.com')
        self.email_input.setStyleSheet(input_style)

        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText('Иван Иванов')
        self.full_name_input.setStyleSheet(input_style)

        self.role_combo = QComboBox()
        self.role_combo.addItems(['developer', 'manager', 'admin'])
        self.role_combo.setStyleSheet(input_style)

        for label_text, widget in [
            ('Имя пользователя *', self.username_input),
            ('Пароль *', self.password_input),
            ('Подтверждение *', self.confirm_password_input),
            ('Email *', self.email_input),
            ('Полное имя *', self.full_name_input),
            ('Роль *', self.role_combo),
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            form.addRow(lbl, widget)

        card_layout.addLayout(form)
        card_layout.addSpacing(8)

        self.register_button = QPushButton('Зарегистрироваться')
        self.register_button.setMinimumHeight(44)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setFont(QFont('Segoe UI', 12, QFont.Bold))
        self.register_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{ background-color: {PRIMARY_DARK}; }}
        """)
        self.register_button.clicked.connect(self.register)
        card_layout.addWidget(self.register_button)

        self.cancel_button = QPushButton('Отмена')
        self.cancel_button.setMinimumHeight(36)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {PRIMARY_COLOR};
                border: none;
                font-weight: 600;
            }}
            QPushButton:hover {{ color: {PRIMARY_DARK}; }}
        """)
        self.cancel_button.clicked.connect(self.reject)
        card_layout.addWidget(self.cancel_button)

        note = QLabel('* — обязательные поля')
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 11px; border: none;")
        card_layout.addWidget(note)

        scroll.setWidget(inner)
        card_inner_layout = QVBoxLayout(card)
        card_inner_layout.setContentsMargins(0, 0, 0, 0)
        card_inner_layout.addWidget(scroll)
        outer.addWidget(card)

        self.username_input.setFocus()

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.email_input.text().strip()
        full_name = self.full_name_input.text().strip()
        role = self.role_combo.currentText()

        if not username or not password or not confirm_password or not email or not full_name:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, заполните все обязательные поля')
            return
        if password != confirm_password:
            QMessageBox.warning(self, 'Ошибка', 'Пароли не совпадают')
            return
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите корректный email')
            return

        result = self.auth_controller.register(username, password, email, full_name, role)
        if result['success']:
            QMessageBox.information(self, 'Успех', 'Регистрация успешно завершена!')
            self.username = username
            self.password = password
            self.accept()
        else:
            QMessageBox.critical(self, 'Ошибка', result['error_message'])
