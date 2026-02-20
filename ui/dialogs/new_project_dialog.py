from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QMessageBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate

from controllers import ProjectController

class NewProjectDialog(QDialog):
    """
    Упрощенный диалог добавления/редактирования проекта
    """
    def __init__(self, parent=None, project=None):
        super().__init__(parent)
        self.project = project
        self.project_controller = ProjectController()

        # Настройка окна
        self.setWindowTitle('Проект' if not self.project else 'Редактирование проекта')
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        # Основной layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите название проекта')

        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText('Введите название клиента')

        self.deadline_input = QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate().addMonths(1))

        self.budget_input = QLineEdit()
        self.budget_input.setPlaceholderText('Введите бюджет проекта')

        form_layout.addRow('Название*:', self.name_input)
        form_layout.addRow('Клиент*:', self.client_input)
        form_layout.addRow('Дедлайн*:', self.deadline_input)
        form_layout.addRow('Бюджет*:', self.budget_input)

        layout.addLayout(form_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.validate_and_accept)

        self.cancel_button = QPushButton('Отмена')
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)

        # Заполнение полей, если редактируем существующий проект
        if self.project:
            self.name_input.setText(self.project.name)
            self.client_input.setText(self.project.client)

            if self.project.deadline:
                try:
                    deadline_date = QDate.fromString(self.project.deadline, "yyyy-MM-dd")
                    self.deadline_input.setDate(deadline_date)
                except:
                    pass

            self.budget_input.setText(str(self.project.budget))

    def validate_and_accept(self):
        """
        Проверка данных перед закрытием диалога
        """
        # Проверка заполнения обязательных полей
        if not self.name_input.text():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, заполните название проекта')
            return

        if not self.client_input.text():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, укажите клиента')
            return

        if not self.budget_input.text():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, укажите бюджет проекта')
            return

        # Проверка корректности бюджета
        try:
            budget = float(self.budget_input.text())
            if budget <= 0:
                QMessageBox.warning(self, 'Предупреждение', 'Бюджет должен быть положительным числом')
                return
        except ValueError:
            QMessageBox.warning(self, 'Предупреждение', 'Бюджет должен быть числом')
            return

        # Если все проверки пройдены, закрываем диалог с принятием результата
        self.accept()