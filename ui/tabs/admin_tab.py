from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QMessageBox,
                             QDialog, QFormLayout, QLineEdit, QComboBox, QCheckBox,
                             QInputDialog, QShortcut)

from PyQt5.QtCore import Qt
from controllers.auth_controller import AuthController

class UserEditDialog(QDialog):
    """
    Диалог для добавления/редактирования пользователя
    """
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.auth_controller = AuthController()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Редактирование пользователя" if self.user else "Добавление пользователя")
        self.setMinimumWidth(400)

        layout = QFormLayout()

        # Поля формы
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.email_edit = QLineEdit()
        self.full_name_edit = QLineEdit()

        self.role_combo = QComboBox()
        self.role_combo.addItems(['admin', 'manager', 'developer'])

        self.is_active_check = QCheckBox()
        self.is_active_check.setChecked(True)

        # Заполнение полей, если редактируем существующего пользователя
        if self.user:
            self.username_edit.setText(self.user.username)
            self.email_edit.setText(self.user.email)
            self.full_name_edit.setText(self.user.full_name)
            self.role_combo.setCurrentText(self.user.role)
            self.is_active_check.setChecked(self.user.is_active)

            # Для существующего пользователя пароль не показываем
            self.password_edit.setPlaceholderText("Оставьте пустым, чтобы не менять")

        # Добавление полей в форму
        layout.addRow("Имя пользователя:", self.username_edit)
        layout.addRow("Пароль:", self.password_edit)
        layout.addRow("Email:", self.email_edit)
        layout.addRow("Полное имя:", self.full_name_edit)
        layout.addRow("Роль:", self.role_combo)
        layout.addRow("Активен:", self.is_active_check)

        # Кнопки
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")

        self.save_button.clicked.connect(self.save_user)
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow("", button_layout)
        self.setLayout(layout)

    def save_user(self):
        """
        Сохранение пользователя
        """
        username = self.username_edit.text()
        password = self.password_edit.text()
        email = self.email_edit.text()
        full_name = self.full_name_edit.text()
        role = self.role_combo.currentText()
        is_active = self.is_active_check.isChecked()

        # Проверка обязательных полей
        if not username or not email or not full_name:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля")
            return

        try:
            if self.user:  # Редактирование существующего пользователя
                data = {
                    'username': username,
                    'email': email,
                    'full_name': full_name,
                    'role': role,
                    'is_active': is_active
                }

                # Добавляем пароль только если он был введен
                if password:
                    data['password'] = password

                result = self.auth_controller.update_user(self.user.id, data)
                if result:
                    QMessageBox.information(self, "Успех", "Пользователь успешно обновлен")
                    self.accept()
            else:  # Создание нового пользователя
                if not password:
                    QMessageBox.warning(self, "Ошибка", "Пароль обязателен для нового пользователя")
                    return

                result = self.auth_controller.register(
                    username=username,
                    password=password,
                    email=email,
                    full_name=full_name,
                    role=role
                )

                if result:
                    QMessageBox.information(self, "Успех", "Пользователь успешно создан")
                    self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить пользователя: {str(e)}")


class AdminTab(QWidget):
    """
    Вкладка администрирования системы
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.auth_controller = AuthController()
        self.init_ui()
        self.load_users()

    def init_ui(self):
        """
        Инициализация интерфейса
        """
        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("Управление пользователями")
        title_label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(title_label)

        # Таблица пользователей
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(["ID", "Имя пользователя", "Email", "Полное имя", "Роль", "Активен"])
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.setSelectionMode(QTableWidget.SingleSelection)
        self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.users_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.users_table)

        # Кнопки управления
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить пользователя")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.reset_password_button = QPushButton("Сбросить пароль")
        self.refresh_button = QPushButton("Обновить")

        self.add_button.clicked.connect(self.add_item)
        self.edit_button.clicked.connect(self.edit_item)
        self.delete_button.clicked.connect(self.delete_item)
        self.reset_password_button.clicked.connect(self.reset_password)
        self.refresh_button.clicked.connect(self.refresh_data)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.reset_password_button)
        button_layout.addWidget(self.refresh_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.reset_password_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        self.reset_password_shortcut.activated.connect(self.reset_password)

    def load_users(self):
        """
        Загрузка списка пользователей
        """
        try:
            result = self.auth_controller.get_all_users()

            # Проверяем, что результат - это словарь с ключом 'success'
            if isinstance(result, dict) and result.get('success'):
                users = result['data']

                self.users_table.setRowCount(0)

                for row, user in enumerate(users):
                    self.users_table.insertRow(row)
                    self.users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                    self.users_table.setItem(row, 1, QTableWidgetItem(user.username))
                    self.users_table.setItem(row, 2, QTableWidgetItem(user.email))
                    self.users_table.setItem(row, 3, QTableWidgetItem(user.full_name))
                    self.users_table.setItem(row, 4, QTableWidgetItem(user.role))

                    is_active_item = QTableWidgetItem()
                    is_active_item.setCheckState(Qt.Checked if user.is_active else Qt.Unchecked)
                    self.users_table.setItem(row, 5, is_active_item)

                    # Сохраняем объект пользователя в первой ячейке
                    self.users_table.item(row, 0).setData(Qt.UserRole, user)
            else:
                # Если результат не соответствует ожидаемому формату
                error_message = result.get('error_message') if isinstance(result, dict) else str(result)
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список пользователей: {error_message}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список пользователей: {str(e)}")

    def get_selected_user(self):
        """
        Получение выбранного пользователя
        """
        selected_rows = self.users_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите пользователя")
            return None

        row = selected_rows[0].row()
        user = self.users_table.item(row, 0).data(Qt.UserRole)
        return user

    def add_item(self):
        """
        Добавление нового пользователя
        """
        dialog = UserEditDialog(self)
        if dialog.exec_():
            self.load_users()

    def edit_item(self):
        """
        Редактирование выбранного пользователя
        """
        user = self.get_selected_user()
        if user:
            dialog = UserEditDialog(self, user)
            if dialog.exec_():
                self.load_users()

    def delete_item(self):
        """
        Удаление выбранного пользователя
        """
        user = self.get_selected_user()
        if not user:
            return

        # Проверка, не пытается ли пользователь удалить самого себя
        if user.id == self.user.id:
            QMessageBox.warning(self, "Предупреждение", "Вы не можете удалить свою учетную запись")
            return

        reply = QMessageBox.question(
            self, 'Подтверждение', f'Вы уверены, что хотите удалить пользователя {user.username}?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                result = self.auth_controller.delete_user(user.id)
                if result:
                    QMessageBox.information(self, "Успех", "Пользователь успешно удален")
                    self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {str(e)}")

    def reset_password(self):
        """
        Сброс пароля выбранного пользователя
        """
        user = self.get_selected_user()
        if not user:
            return

        from PyQt5.QtWidgets import QInputDialog, QLineEdit
        new_password, ok = QInputDialog.getText(
            self, 'Сброс пароля', 'Введите новый пароль:',
            QLineEdit.Password  # Use QLineEdit.Password instead of QInputDialog.Password
        )

        if ok and new_password:
            try:
                result = self.auth_controller.reset_password(user.id, new_password)
                if result:
                    QMessageBox.information(self, "Успех", "Пароль успешно сброшен")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сбросить пароль: {str(e)}")


    def refresh_data(self):
        """
        Обновление данных
        """
        self.load_users()