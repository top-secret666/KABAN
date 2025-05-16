import sys
import os
import sqlite3
import csv
import hashlib
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QPushButton, QHeaderView,
                             QMessageBox, QDateEdit, QDoubleSpinBox, QSpinBox, QCheckBox,
                             QGroupBox, QSplitter, QFrame, QDialog, QDialogButtonBox,
                             QFileDialog, QGridLayout, QInputDialog, QAction, QMenu)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont, QColor


class DatabaseManager:
    def __init__(self, db_path='database/kabanmanagement_it-projects.sqlite'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.init_users_table()

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None

    def close(self):
        if self.connection:
            self.connection.close()

    def init_users_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.execute_query(query)

        admin = self.fetch_one("SELECT * FROM users WHERE username = ?", ("admin",))
        if not admin:
            password_hash = hashlib.sha256("admin".encode()).hexdigest()
            self.execute_query(
                "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                ("admin", password_hash, "Administrator", "admin")
            )
            print("Default admin user created")


class LoginDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.authenticated_user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация")
        self.setFixedSize(350, 200)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Имя пользователя:", self.username_edit)
        form_layout.addRow("Пароль:", self.password_edit)

        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()

        if not username or not password:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите имя пользователя и пароль")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user = self.db_manager.fetch_one(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )

        if user:
            self.authenticated_user = dict(user)
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверное имя пользователя или пароль")


class UserManagementDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Управление пользователями")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["ID", "Имя пользователя", "Полное имя", "Роль", "Дата создания"])
        self.user_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить пользователя")
        self.add_button.clicked.connect(self.add_user)
        self.edit_button = QPushButton("Изменить пользователя")
        self.edit_button.clicked.connect(self.edit_user)
        self.delete_button = QPushButton("Удалить пользователя")
        self.delete_button.clicked.connect(self.delete_user)
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.accept)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.close_button)

        layout.addWidget(self.user_table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        users = self.db_manager.fetch_all("SELECT * FROM users ORDER BY username")

        self.user_table.setRowCount(0)
        for row, user in enumerate(users):
            self.user_table.insertRow(row)
            self.user_table.setItem(row, 0, QTableWidgetItem(str(user['id'])))
            self.user_table.setItem(row, 1, QTableWidgetItem(user['username']))
            self.user_table.setItem(row, 2, QTableWidgetItem(user['full_name'] or ""))
            self.user_table.setItem(row, 3, QTableWidgetItem(user['role']))
            self.user_table.setItem(row, 4, QTableWidgetItem(user['created_at']))

    def add_user(self):
        dialog = UserDialog(self.db_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()

    def edit_user(self):
        selected_rows = self.user_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите пользователя для редактирования")
            return

        row = selected_rows[0].row()
        user_id = int(self.user_table.item(row, 0).text())

        dialog = UserDialog(self.db_manager, self, user_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_users()

    def delete_user(self):
        selected_rows = self.user_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите пользователя для удаления")
            return

        row = selected_rows[0].row()
        user_id = int(self.user_table.item(row, 0).text())
        username = self.user_table.item(row, 1).text()

        if username == "admin":
            QMessageBox.warning(self, "Предупреждение", "Невозможно удалить администратора системы")
            return

        confirm = QMessageBox.question(self, "Подтверждение",
                                       f"Вы уверены, что хотите удалить пользователя '{username}'?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            try:
                self.db_manager.execute_query("DELETE FROM users WHERE id = ?", (user_id,))
                self.load_users()
                QMessageBox.information(self, "Успех", "Пользователь успешно удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя: {str(e)}")


class UserDialog(QDialog):
    def __init__(self, db_manager, parent=None, user_id=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_id = user_id
        self.init_ui()

        if user_id:
            self.load_user()

    def init_ui(self):
        self.setWindowTitle("Пользователь")
        self.setFixedSize(400, 250)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.fullname_edit = QLineEdit()
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin"])

        form_layout.addRow("Имя пользователя*:", self.username_edit)
        form_layout.addRow("Пароль*:", self.password_edit)
        form_layout.addRow("Полное имя:", self.fullname_edit)
        form_layout.addRow("Роль:", self.role_combo)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.save_user)
        button_box.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(QLabel("* - обязательные поля"))
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_user(self):
        user = self.db_manager.fetch_one("SELECT * FROM users WHERE id = ?", (self.user_id,))
        if user:
            self.username_edit.setText(user['username'])
            self.fullname_edit.setText(user['full_name'] or "")
            self.role_combo.setCurrentText(user['role'])

            self.password_edit.setPlaceholderText("Оставьте пустым, чтобы не менять")

    def save_user(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        fullname = self.fullname_edit.text().strip()
        role = self.role_combo.currentText()

        if not username:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите имя пользователя")
            return

        try:
            if self.user_id:
                if password:
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    self.db_manager.execute_query(
                        "UPDATE users SET username = ?, password_hash = ?, full_name = ?, role = ? WHERE id = ?",
                        (username, password_hash, fullname, role, self.user_id)
                    )
                else:
                    self.db_manager.execute_query(
                        "UPDATE users SET username = ?, full_name = ?, role = ? WHERE id = ?",
                        (username, fullname, role, self.user_id)
                    )
            else:
                if not password:
                    QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите пароль")
                    return

                password_hash = hashlib.sha256(password.encode()).hexdigest()
                self.db_manager.execute_query(
                    "INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                    (username, password_hash, fullname, role)
                )

            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить пользователя: {str(e)}")


class DeveloperForm(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_id = None
        self.init_ui()

    def init_ui(self):
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.position_combo = QComboBox()
        self.position_combo.addItems(['backend', 'frontend', 'QA'])
        self.rate_spin = QDoubleSpinBox()
        self.rate_spin.setRange(0, 10000)
        self.rate_spin.setSingleStep(100)
        self.rate_spin.setValue(1000)

        form_layout.addRow("ФИО:", self.name_edit)
        form_layout.addRow("Должность:", self.position_combo)
        form_layout.addRow("Почасовая ставка:", self.rate_spin)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.update_button = QPushButton("Обновить")
        self.delete_button = QPushButton("Удалить")
        self.clear_button = QPushButton("Очистить")
        self.export_button = QPushButton("Экспорт в CSV")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Ставка"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по ФИО...")
        self.search_button = QPushButton("Поиск")
        self.reset_search_button = QPushButton("Сбросить")

        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_search_button)

        main_layout = QVBoxLayout()
        form_group = QGroupBox("Данные разработчика")
        form_group.setLayout(form_layout)

        main_layout.addWidget(form_group)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_developer)
        self.update_button.clicked.connect(self.update_developer)
        self.delete_button.clicked.connect(self.delete_developer)
        self.clear_button.clicked.connect(self.clear_form)
        self.export_button.clicked.connect(self.export_to_csv)
        self.table.itemClicked.connect(self.select_developer)
        self.search_button.clicked.connect(self.search_developers)
        self.reset_search_button.clicked.connect(self.load_developers)

        self.load_developers()

    def load_developers(self):
        developers = self.db_manager.fetch_all("SELECT * FROM developers ORDER BY full_name")
        self.populate_table(developers)

    def populate_table(self, developers):
        self.table.setRowCount(0)
        for row, developer in enumerate(developers):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(developer['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(developer['full_name']))
            self.table.setItem(row, 2, QTableWidgetItem(developer['position']))
            self.table.setItem(row, 3, QTableWidgetItem(str(developer['hourly_rate'])))

    def add_developer(self):
        name = self.name_edit.text().strip()
        position = self.position_combo.currentText()
        rate = self.rate_spin.value()

        if not name:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите ФИО разработчика")
            return

        try:
            existing = self.db_manager.fetch_one(
                "SELECT id FROM developers WHERE full_name = ?",
                (name,)
            )

            if existing:
                query = "UPDATE developers SET position = ?, hourly_rate = ? WHERE id = ?"
                self.db_manager.execute_query(query, (position, rate, existing['id']))
                QMessageBox.information(self, "Успех", "Данные существующего разработчика обновлены")
            else:
                query = "INSERT INTO developers (full_name, position, hourly_rate) VALUES (?, ?, ?)"
                self.db_manager.execute_query(query, (name, position, rate))
                QMessageBox.information(self, "Успех", "Разработчик успешно добавлен")

            self.load_developers()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить/обновить разработчика: {str(e)}")

    def update_developer(self):
        if not self.current_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите разработчика для обновления")
            return

        name = self.name_edit.text().strip()
        position = self.position_combo.currentText()
        rate = self.rate_spin.value()

        if not name:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, введите ФИО разработчика")
            return

        try:
            query = "UPDATE developers SET full_name = ?, position = ?, hourly_rate = ? WHERE id = ?"
            self.db_manager.execute_query(query, (name, position, rate, self.current_id))
            self.load_developers()
            self.clear_form()
            QMessageBox.information(self, "Успех", "Данные разработчика успешно обновлены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные разработчика: {str(e)}")

    def delete_developer(self):
        if not self.current_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите разработчика для удаления")
            return

        tasks = self.db_manager.fetch_all("SELECT COUNT(*) as count FROM tasks WHERE developer_id = ?",
                                          (self.current_id,))
        if tasks and tasks[0]['count'] > 0:
            QMessageBox.warning(self, "Предупреждение",
                                f"Невозможно удалить разработчика, так как у него есть {tasks[0]['count']} назначенных задач")
            return

        confirm = QMessageBox.question(self, "Подтверждение",
                                       "Вы уверены, что хотите удалить этого разработчика?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            try:
                self.db_manager.execute_query("DELETE FROM developers WHERE id = ?", (self.current_id,))
                self.load_developers()
                self.clear_form()
                QMessageBox.information(self, "Успех", "Разработчик успешно удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить разработчика: {str(e)}")

    def select_developer(self, item):
        row = item.row()
        self.current_id = int(self.table.item(row, 0).text())
        self.name_edit.setText(self.table.item(row, 1).text())
        self.position_combo.setCurrentText(self.table.item(row, 2).text())
        self.rate_spin.setValue(float(self.table.item(row, 3).text()))

    def clear_form(self):
        self.current_id = None
        self.name_edit.clear()
        self.position_combo.setCurrentIndex(0)
        self.rate_spin.setValue(1000)

    def search_developers(self):
        search_term = self.search_edit.text().strip()
        if not search_term:
            self.load_developers()
            return

        developers = self.db_manager.fetch_all(
            "SELECT * FROM developers WHERE full_name LIKE ? ORDER BY full_name",
            (f"%{search_term}%",)
        )
        self.populate_table(developers)

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", "", "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            developers = self.db_manager.fetch_all("SELECT * FROM developers ORDER BY full_name")

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'ФИО', 'Должность', 'Почасовая ставка'])

                for developer in developers:
                    writer.writerow([
                        developer['id'],
                        developer['full_name'],
                        developer['position'],
                        developer['hourly_rate']
                    ])

            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")


class ProjectForm(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_id = None
        self.init_ui()

    def init_ui(self):
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.client_edit = QLineEdit()
        self.deadline_edit = QDateEdit()
        self.deadline_edit.setCalendarPopup(True)
        self.deadline_edit.setDate(QDate.currentDate().addMonths(1))
        self.budget_spin = QDoubleSpinBox()
        self.budget_spin.setRange(0, 10000000)
        self.budget_spin.setSingleStep(10000)
        self.budget_spin.setValue(100000)

        form_layout.addRow("Название проекта:", self.name_edit)
        form_layout.addRow("Клиент:", self.client_edit)
        form_layout.addRow("Срок сдачи:", self.deadline_edit)
        form_layout.addRow("Бюджет:", self.budget_spin)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.update_button = QPushButton("Обновить")
        self.delete_button = QPushButton("Удалить")
        self.clear_button = QPushButton("Очистить")
        self.export_button = QPushButton("Экспорт в CSV")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Клиент", "Срок сдачи", "Бюджет"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по названию или клиенту...")
        self.search_button = QPushButton("Поиск")
        self.reset_search_button = QPushButton("Сбросить")

        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_search_button)

        main_layout = QVBoxLayout()
        form_group = QGroupBox("Данные проекта")
        form_group.setLayout(form_layout)

        main_layout.addWidget(form_group)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_project)
        self.update_button.clicked.connect(self.update_project)
        self.delete_button.clicked.connect(self.delete_project)
        self.clear_button.clicked.connect(self.clear_form)
        self.export_button.clicked.connect(self.export_to_csv)
        self.table.itemClicked.connect(self.select_project)
        self.search_button.clicked.connect(self.search_projects)
        self.reset_search_button.clicked.connect(self.load_projects)

        self.load_projects()

    def load_projects(self):
        projects = self.db_manager.fetch_all("SELECT * FROM projects ORDER BY deadline")
        self.populate_table(projects)

    def populate_table(self, projects):
        self.table.setRowCount(0)
        for row, project in enumerate(projects):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(project['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(project['name']))
            self.table.setItem(row, 2, QTableWidgetItem(project['client']))

            deadline = QDate.fromString(project['deadline'], "yyyy-MM-dd")
            self.table.setItem(row, 3, QTableWidgetItem(deadline.toString("dd.MM.yyyy")))

            self.table.setItem(row, 4, QTableWidgetItem(str(project['budget'])))

    def add_project(self):
        name = self.name_edit.text().strip()
        client = self.client_edit.text().strip()
        deadline = self.deadline_edit.date().toString("yyyy-MM-dd")
        budget = self.budget_spin.value()

        if not name or not client:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните название проекта и клиента")
            return

        try:
            existing = self.db_manager.fetch_one(
                "SELECT id FROM projects WHERE name = ? AND client = ?",
                (name, client)
            )

            if existing:
                query = "UPDATE projects SET deadline = ?, budget = ? WHERE id = ?"
                self.db_manager.execute_query(query, (deadline, budget, existing['id']))
                QMessageBox.information(self, "Успех", "Данные существующего проекта обновлены")
            else:
                query = "INSERT INTO projects (name, client, deadline, budget, status) VALUES (?, ?, ?, ?, 'в работе')"
                self.db_manager.execute_query(query, (name, client, deadline, budget))
                QMessageBox.information(self, "Успех", "Проект успешно добавлен")

            self.load_projects()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить/обновить проект: {str(e)}")

    def update_project(self):
        if not self.current_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите проект для обновления")
            return

        name = self.name_edit.text().strip()
        client = self.client_edit.text().strip()
        deadline = self.deadline_edit.date().toString("yyyy-MM-dd")
        budget = self.budget_spin.value()

        if not name or not client:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните название проекта и клиента")
            return

        try:
            query = "UPDATE projects SET name = ?, client = ?, deadline = ?, budget = ? WHERE id = ?"
            self.db_manager.execute_query(query, (name, client, deadline, budget, self.current_id))
            self.load_projects()
            self.clear_form()
            QMessageBox.information(self, "Успех", "Данные проекта успешно обновлены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные проекта: {str(e)}")

    def delete_project(self):
        if not self.current_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите проект для удаления")
            return

        tasks = self.db_manager.fetch_all("SELECT COUNT(*) as count FROM tasks WHERE project_id = ?",
                                          (self.current_id,))
        if tasks and tasks[0]['count'] > 0:
            confirm = QMessageBox.question(self, "Подтверждение",
                                           f"Проект содержит {tasks[0]['count']} задач. Удалить проект вместе с задачами?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.No:
                return
        else:
            confirm = QMessageBox.question(self, "Подтверждение",
                                           "Вы уверены, что хотите удалить этот проект?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.No:
                return

        try:
            self.db_manager.execute_query("DELETE FROM tasks WHERE project_id = ?", (self.current_id,))
            self.db_manager.execute_query("DELETE FROM projects WHERE id = ?", (self.current_id,))
            self.load_projects()
            self.clear_form()
            QMessageBox.information(self, "Успех", "Проект успешно удален")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить проект: {str(e)}")

    def select_project(self, item):
        row = item.row()
        self.current_id = int(self.table.item(row, 0).text())
        self.name_edit.setText(self.table.item(row, 1).text())
        self.client_edit.setText(self.table.item(row, 2).text())

        date_str = self.table.item(row, 3).text()
        date = QDate.fromString(date_str, "dd.MM.yyyy")
        self.deadline_edit.setDate(date)

        self.budget_spin.setValue(float(self.table.item(row, 4).text()))

    def clear_form(self):
        self.current_id = None
        self.name_edit.clear()
        self.client_edit.clear()
        self.deadline_edit.setDate(QDate.currentDate().addMonths(1))
        self.budget_spin.setValue(100000)

    def search_projects(self):
        search_term = self.search_edit.text().strip()
        if not search_term:
            self.load_projects()
            return

        projects = self.db_manager.fetch_all(
            "SELECT * FROM projects WHERE name LIKE ? OR client LIKE ? ORDER BY deadline",
            (f"%{search_term}%", f"%{search_term}%")
        )
        self.populate_table(projects)

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", "", "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            projects = self.db_manager.fetch_all("SELECT * FROM projects ORDER BY deadline")

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Название', 'Клиент', 'Срок сдачи', 'Бюджет', 'Статус'])

                for project in projects:
                    deadline = QDate.fromString(project['deadline'], "yyyy-MM-dd").toString("dd.MM.yyyy")
                    writer.writerow([
                        project['id'],
                        project['name'],
                        project['client'],
                        deadline,
                        project['budget'],
                        project['status']
                    ])

            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")


class TaskForm(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.current_id = None
        self.init_ui()

    def init_ui(self):
        form_layout = QFormLayout()

        self.project_combo = QComboBox()
        self.developer_combo = QComboBox()
        self.description_edit = QLineEdit()
        self.status_combo = QComboBox()
        self.status_combo.addItems(['в работе', 'завершено'])
        self.hours_spin = QDoubleSpinBox()
        self.hours_spin.setRange(0, 1000)
        self.hours_spin.setSingleStep(0.5)

        form_layout.addRow("Проект:", self.project_combo)
        form_layout.addRow("Разработчик:", self.developer_combo)
        form_layout.addRow("Описание:", self.description_edit)
        form_layout.addRow("Статус:", self.status_combo)
        form_layout.addRow("Затраченные часы:", self.hours_spin)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.update_button = QPushButton("Обновить")
        self.delete_button = QPushButton("Удалить")
        self.clear_button = QPushButton("Очистить")
        self.export_button = QPushButton("Экспорт в CSV")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по описанию...")
        self.project_filter = QComboBox()
        self.project_filter.addItem("Все проекты", None)
        self.developer_filter = QComboBox()
        self.developer_filter.addItem("Все разработчики", None)
        self.search_button = QPushButton("Поиск")
        self.reset_search_button = QPushButton("Сбросить")

        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(self.project_filter)
        search_layout.addWidget(self.developer_filter)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.reset_search_button)

        main_layout = QVBoxLayout()
        form_group = QGroupBox("Данные задачи")
        form_group.setLayout(form_layout)

        main_layout.addWidget(form_group)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_task)
        self.update_button.clicked.connect(self.update_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.clear_button.clicked.connect(self.clear_form)
        self.export_button.clicked.connect(self.export_to_csv)
        self.table.itemClicked.connect(self.select_task)
        self.search_button.clicked.connect(self.search_tasks)
        self.reset_search_button.clicked.connect(self.load_tasks)

        self.load_projects_and_developers()
        self.load_tasks()

    def load_projects_and_developers(self):
        self.project_combo.clear()
        self.project_filter.clear()
        self.project_filter.addItem("Все проекты", None)

        projects = self.db_manager.fetch_all("SELECT id, name FROM projects ORDER BY name")
        for project in projects:
            self.project_combo.addItem(project['name'], project['id'])
            self.project_filter.addItem(project['name'], project['id'])

        self.developer_combo.clear()
        self.developer_filter.clear()
        self.developer_filter.addItem("Все разработчики", None)

        developers = self.db_manager.fetch_all("SELECT id, full_name FROM developers ORDER BY full_name")
        for developer in developers:
            self.developer_combo.addItem(developer['full_name'], developer['id'])
            self.developer_filter.addItem(developer['full_name'], developer['id'])

    def load_tasks(self):
        query = """
            SELECT t.id, t.description, t.status, t.hours_worked, 
                   p.name as project_name, d.full_name as developer_name,
                   t.project_id, t.developer_id
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            JOIN developers d ON t.developer_id = d.id
            ORDER BY t.id DESC
        """
        tasks = self.db_manager.fetch_all(query)
        self.populate_table(tasks)

    def populate_table(self, tasks):
        self.table.setRowCount(0)
        for row, task in enumerate(tasks):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(task['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(task['project_name']))
            self.table.setItem(row, 2, QTableWidgetItem(task['developer_name']))
            self.table.setItem(row, 3, QTableWidgetItem(task['description']))
            self.table.setItem(row, 4, QTableWidgetItem(task['status']))
            self.table.setItem(row, 5, QTableWidgetItem(str(task['hours_worked'])))

            self.table.item(row, 1).setData(Qt.UserRole, task['project_id'])
            self.table.item(row, 2).setData(Qt.UserRole, task['developer_id'])

    def add_task(self):
        project_id = self.project_combo.currentData()
        developer_id = self.developer_combo.currentData()
        description = self.description_edit.text().strip()
        status = self.status_combo.currentText()
        hours = self.hours_spin.value()

        if not project_id or not developer_id or not description:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля")
            return

        try:
            existing = self.db_manager.fetch_one(
                "SELECT id FROM tasks WHERE project_id = ? AND developer_id = ? AND description = ?",
                (project_id, developer_id, description)
            )

            if existing:
                query = "UPDATE tasks SET status = ?, hours_worked = ? WHERE id = ?"
                self.db_manager.execute_query(query, (status, hours, existing['id']))
                QMessageBox.information(self, "Успех", "Данные существующей задачи обновлены")
            else:
                query = """
                    INSERT INTO tasks (project_id, developer_id, description, status, hours_worked) 
                    VALUES (?, ?, ?, ?, ?)
                """
                self.db_manager.execute_query(query, (project_id, developer_id, description, status, hours))
                QMessageBox.information(self, "Успех", "Задача успешно добавлена")

            self.load_tasks()
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить/обновить задачу: {str(e)}")

    def update_task(self):
        if not self.current_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите задачу для обновления")
            return

        project_id = self.project_combo.currentData()
        developer_id = self.developer_combo.currentData()
        description = self.description_edit.text().strip()
        status = self.status_combo.currentText()
        hours = self.hours_spin.value()

        if not project_id or not developer_id or not description:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, заполните все обязательные поля")
            return

        try:
            query = """
                UPDATE tasks 
                SET project_id = ?, developer_id = ?, description = ?, status = ?, hours_worked = ? 
                WHERE id = ?
            """
            self.db_manager.execute_query(query,
                                          (project_id, developer_id, description, status, hours, self.current_id))
            self.load_tasks()
            self.clear_form()
            QMessageBox.information(self, "Успех", "Данные задачи успешно обновлены")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные задачи: {str(e)}")

    def delete_task(self):
        if not self.current_id:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите задачу для удаления")
            return

        confirm = QMessageBox.question(self, "Подтверждение",
                                       "Вы уверены, что хотите удалить эту задачу?",
                                       QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            try:
                self.db_manager.execute_query("DELETE FROM tasks WHERE id = ?", (self.current_id,))
                self.load_tasks()
                self.clear_form()
                QMessageBox.information(self, "Успех", "Задача успешно удалена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить задачу: {str(e)}")

    def select_task(self, item):
        row = item.row()
        self.current_id = int(self.table.item(row, 0).text())

        project_id = self.table.item(row, 1).data(Qt.UserRole)
        developer_id = self.table.item(row, 2).data(Qt.UserRole)

        index = self.project_combo.findData(project_id)
        if index >= 0:
            self.project_combo.setCurrentIndex(index)

        index = self.developer_combo.findData(developer_id)
        if index >= 0:
            self.developer_combo.setCurrentIndex(index)

        self.description_edit.setText(self.table.item(row, 3).text())
        self.status_combo.setCurrentText(self.table.item(row, 4).text())
        self.hours_spin.setValue(float(self.table.item(row, 5).text()))

    def clear_form(self):
        self.current_id = None
        if self.project_combo.count() > 0:
            self.project_combo.setCurrentIndex(0)
        if self.developer_combo.count() > 0:
            self.developer_combo.setCurrentIndex(0)
        self.description_edit.clear()
        self.status_combo.setCurrentIndex(0)
        self.hours_spin.setValue(0)

    def search_tasks(self):
        search_term = self.search_edit.text().strip()
        project_id = self.project_filter.currentData()
        developer_id = self.developer_filter.currentData()

        query = """
            SELECT t.id, t.description, t.status, t.hours_worked, 
                   p.name as project_name, d.full_name as developer_name,
                   t.project_id, t.developer_id
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            JOIN developers d ON t.developer_id = d.id
            WHERE 1=1
        """
        params = []

        if search_term:
            query += " AND t.description LIKE ?"
            params.append(f"%{search_term}%")

        if project_id:
            query += " AND t.project_id = ?"
            params.append(project_id)

        if developer_id:
            query += " AND t.developer_id = ?"
            params.append(developer_id)

        query += " ORDER BY t.id DESC"

        tasks = self.db_manager.fetch_all(query, params)
        self.populate_table(tasks)

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт данных", "", "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            query = """
                SELECT t.id, p.name as project_name, d.full_name as developer_name,
                       t.description, t.status, t.hours_worked, d.hourly_rate,
                       (t.hours_worked * d.hourly_rate) as cost
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                JOIN developers d ON t.developer_id = d.id
                ORDER BY t.id
            """
            tasks = self.db_manager.fetch_all(query)

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'ID', 'Проект', 'Разработчик', 'Описание', 'Статус',
                    'Часы', 'Ставка', 'Стоимость'
                ])

                for task in tasks:
                    writer.writerow([
                        task['id'],
                        task['project_name'],
                        task['developer_name'],
                        task['description'],
                        task['status'],
                        task['hours_worked'],
                        task['hourly_rate'],
                        task['cost']
                    ])

            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")


class StatisticsTab(QWidget):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        project_group = QGroupBox("Статистика по проектам")
        project_layout = QVBoxLayout()

        self.project_table = QTableWidget()
        self.project_table.setColumnCount(6)
        self.project_table.setHorizontalHeaderLabels([
            "Проект", "Клиент", "Срок сдачи", "Бюджет",
            "Выполнено задач", "Затраты"
        ])
        self.project_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.project_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        export_project_button = QPushButton("Экспорт статистики проектов")
        export_project_button.clicked.connect(self.export_project_stats)

        project_layout.addWidget(self.project_table)
        project_layout.addWidget(export_project_button)
        project_group.setLayout(project_layout)

        developer_group = QGroupBox("Статистика по разработчикам")
        developer_layout = QVBoxLayout()

        self.developer_table = QTableWidget()
        self.developer_table.setColumnCount(5)
        self.developer_table.setHorizontalHeaderLabels([
            "Разработчик", "Должность", "Ставка",
            "Выполнено задач", "Общие часы"
        ])
        self.developer_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        export_developer_button = QPushButton("Экспорт статистики разработчиков")
        export_developer_button.clicked.connect(self.export_developer_stats)

        developer_layout.addWidget(self.developer_table)
        developer_layout.addWidget(export_developer_button)
        developer_group.setLayout(developer_layout)

        refresh_button = QPushButton("Обновить статистику")
        refresh_button.clicked.connect(self.load_statistics)

        main_layout.addWidget(project_group)
        main_layout.addWidget(developer_group)
        main_layout.addWidget(refresh_button)

        self.setLayout(main_layout)

        self.load_statistics()

    def load_statistics(self):
        self.load_project_statistics()
        self.load_developer_statistics()

    def load_project_statistics(self):
        query = """
            SELECT 
                p.id, p.name, p.client, p.deadline, p.budget,
                COUNT(t.id) as total_tasks,
                SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                SUM(t.hours_worked) as total_hours,
                SUM(t.hours_worked * d.hourly_rate) as labor_cost
            FROM projects p
            LEFT JOIN tasks t ON p.id = t.project_id
            LEFT JOIN developers d ON t.developer_id = d.id
            GROUP BY p.id
            ORDER BY p.deadline
        """

        projects = self.db_manager.fetch_all(query)

        self.project_table.setRowCount(0)
        for row, project in enumerate(projects):
            self.project_table.insertRow(row)
            self.project_table.setItem(row, 0, QTableWidgetItem(project['name']))
            self.project_table.setItem(row, 1, QTableWidgetItem(project['client']))

            deadline = QDate.fromString(project['deadline'], "yyyy-MM-dd")
            self.project_table.setItem(row, 2, QTableWidgetItem(deadline.toString("dd.MM.yyyy")))

            self.project_table.setItem(row, 3, QTableWidgetItem(f"{project['budget']:.2f}"))

            completion = f"{project['completed_tasks']}/{project['total_tasks']}"
            self.project_table.setItem(row, 4, QTableWidgetItem(completion))

            labor_cost = project['labor_cost'] if project['labor_cost'] else 0
            self.project_table.setItem(row, 5, QTableWidgetItem(f"{labor_cost:.2f}"))

            if labor_cost > project['budget']:
                for col in range(6):
                    self.project_table.item(row, col).setBackground(QColor(255, 200, 200))

    def load_developer_statistics(self):
        query = """
            SELECT 
                d.id, d.full_name, d.position, d.hourly_rate,
                COUNT(t.id) as total_tasks,
                SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                SUM(t.hours_worked) as total_hours
            FROM developers d
            LEFT JOIN tasks t ON d.id = t.developer_id
            GROUP BY d.id
            ORDER BY d.full_name
        """

        developers = self.db_manager.fetch_all(query)

        self.developer_table.setRowCount(0)
        for row, developer in enumerate(developers):
            self.developer_table.insertRow(row)
            self.developer_table.setItem(row, 0, QTableWidgetItem(developer['full_name']))
            self.developer_table.setItem(row, 1, QTableWidgetItem(developer['position']))
            self.developer_table.setItem(row, 2, QTableWidgetItem(f"{developer['hourly_rate']:.2f}"))

            completion = f"{developer['completed_tasks']}/{developer['total_tasks']}"
            self.developer_table.setItem(row, 3, QTableWidgetItem(completion))

            total_hours = developer['total_hours'] if developer['total_hours'] else 0
            self.developer_table.setItem(row, 4, QTableWidgetItem(f"{total_hours:.2f}"))

    def export_project_stats(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт статистики проектов", "", "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            query = """
                SELECT 
                    p.id, p.name, p.client, p.deadline, p.budget,
                    COUNT(t.id) as total_tasks,
                    SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                    SUM(t.hours_worked) as total_hours,
                    SUM(t.hours_worked * d.hourly_rate) as labor_cost
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                LEFT JOIN developers d ON t.developer_id = d.id
                GROUP BY p.id
                ORDER BY p.deadline
            """

            projects = self.db_manager.fetch_all(query)

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'ID', 'Название', 'Клиент', 'Срок сдачи', 'Бюджет',
                    'Всего задач', 'Выполнено задач', 'Общие часы', 'Затраты', 'Остаток бюджета'
                ])

                for project in projects:
                    deadline = QDate.fromString(project['deadline'], "yyyy-MM-dd").toString("dd.MM.yyyy")
                    labor_cost = project['labor_cost'] if project['labor_cost'] else 0
                    budget_remaining = project['budget'] - labor_cost

                    writer.writerow([
                        project['id'],
                        project['name'],
                        project['client'],
                        deadline,
                        project['budget'],
                        project['total_tasks'],
                        project['completed_tasks'],
                        project['total_hours'] if project['total_hours'] else 0,
                        labor_cost,
                        budget_remaining
                    ])

            QMessageBox.information(self, "Успех", f"Статистика проектов успешно экспортирована в {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать статистику: {str(e)}")

    def export_developer_stats(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Экспорт статистики разработчиков", "", "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            query = """
                SELECT 
                    d.id, d.full_name, d.position, d.hourly_rate,
                    COUNT(t.id) as total_tasks,
                    SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                    SUM(t.hours_worked) as total_hours,
                    SUM(t.hours_worked * d.hourly_rate) as earnings
                FROM developers d
                LEFT JOIN tasks t ON d.id = t.developer_id
                GROUP BY d.id
                ORDER BY d.full_name
            """

            developers = self.db_manager.fetch_all(query)

            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'ID', 'ФИО', 'Должность', 'Ставка',
                    'Всего задач', 'Выполнено задач', 'Общие часы', 'Заработок'
                ])

                for developer in developers:
                    total_hours = developer['total_hours'] if developer['total_hours'] else 0
                    earnings = developer['earnings'] if developer['earnings'] else 0

                    writer.writerow([
                        developer['id'],
                        developer['full_name'],
                        developer['position'],
                        developer['hourly_rate'],
                        developer['total_tasks'],
                        developer['completed_tasks'],
                        total_hours,
                        earnings
                    ])

            QMessageBox.information(self, "Успех", f"Статистика разработчиков успешно экспортирована в {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать статистику: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kanban Management System")
        self.setGeometry(100, 100, 1200, 800)

        self.create_menu_bar()

        self.tab_widget = QTabWidget()

        self.developer_tab = DeveloperForm(self.db_manager)
        self.project_tab = ProjectForm(self.db_manager)
        self.task_tab = TaskForm(self.db_manager)
        self.statistics_tab = StatisticsTab(self.db_manager)

        self.tab_widget.addTab(self.developer_tab, "Разработчики")
        self.tab_widget.addTab(self.project_tab, "Проекты")
        self.tab_widget.addTab(self.task_tab, "Задачи")
        self.tab_widget.addTab(self.statistics_tab, "Статистика")

        self.setCentralWidget(self.tab_widget)

        if self.user:
            self.setWindowTitle(f"Kanban Management System - {self.user['full_name']} ({self.user['username']})")

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Файл")

        export_action = QAction("Экспорт всех данных", self)
        export_action.triggered.connect(self.export_all_data)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        if self.user and self.user['role'] == 'admin':
            admin_menu = menubar.addMenu("Администрирование")

            users_action = QAction("Управление пользователями", self)
            users_action.triggered.connect(self.manage_users)
            admin_menu.addAction(users_action)

        help_menu = menubar.addMenu("Справка")

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def export_all_data(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для экспорта")
        if not folder_path:
            return

        try:
            developers_path = os.path.join(folder_path, "developers.csv")
            developers = self.db_manager.fetch_all("SELECT * FROM developers ORDER BY full_name")

            with open(developers_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'ФИО', 'Должность', 'Почасовая ставка'])
                for developer in developers:
                    writer.writerow([
                        developer['id'],
                        developer['full_name'],
                        developer['position'],
                        developer['hourly_rate']
                    ])

            projects_path = os.path.join(folder_path, "projects.csv")
            projects = self.db_manager.fetch_all("SELECT * FROM projects ORDER BY deadline")

            with open(projects_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Название', 'Клиент', 'Срок сдачи', 'Бюджет', 'Статус'])
                for project in projects:
                    deadline = QDate.fromString(project['deadline'], "yyyy-MM-dd").toString("dd.MM.yyyy")
                    writer.writerow([
                        project['id'],
                        project['name'],
                        project['client'],
                        deadline,
                        project['budget'],
                        project['status']
                    ])

            tasks_path = os.path.join(folder_path, "tasks.csv")
            query = """
                SELECT t.id, p.name as project_name, d.full_name as developer_name,
                       t.description, t.status, t.hours_worked, d.hourly_rate,
                       (t.hours_worked * d.hourly_rate) as cost
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                JOIN developers d ON t.developer_id = d.id
                ORDER BY t.id
            """
            tasks = self.db_manager.fetch_all(query)

            with open(tasks_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'ID', 'Проект', 'Разработчик', 'Описание', 'Статус',
                    'Часы', 'Ставка', 'Стоимость'
                ])
                for task in tasks:
                    writer.writerow([
                        task['id'],
                        task['project_name'],
                        task['developer_name'],
                        task['description'],
                        task['status'],
                        task['hours_worked'],
                        task['hourly_rate'],
                        task['cost']
                    ])

            QMessageBox.information(self, "Успех", f"Все данные успешно экспортированы в папку {folder_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def manage_users(self):
        dialog = UserManagementDialog(self.db_manager, self)
        dialog.exec_()

    def show_about(self):
        QMessageBox.about(self, "О программе",
                          "Kanban Management System\n\n"
                          "Версия: 1.0\n"
                          "Система управления IT-проектами\n\n"
                          "© 2023 Все права защищены")

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db_manager = DatabaseManager()

    login_dialog = LoginDialog(db_manager)
    if login_dialog.exec_() == QDialog.Accepted:
        window = MainWindow(login_dialog.authenticated_user)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)