from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QMessageBox, QDateEdit)
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator
from PyQt5.QtCore import Qt, QDate

from controllers import ProjectController


class ProjectDialog(QDialog):
    """
    Диалог добавления/редактирования проекта
    """

    def __init__(self, parent=None, project=None):
        super().__init__(parent)
        self.project = project
        self.project_controller = ProjectController()
        self.init_ui()

    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('Проект' if not self.project else 'Редактирование проекта')
        self.setWindowIcon(QIcon('ui/resources/icons/project.png'))
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowTitleHint)

        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

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
        self.budget_input.setValidator(QDoubleValidator(0, 1000000000, 2))

        form_layout.addRow('Название*:', self.name_input)
        form_layout.addRow('Клиент*:', self.client_input)
        form_layout.addRow('Дедлайн*:', self.deadline_input)
        form_layout.addRow('Бюджет*:', self.budget_input)

        main_layout.addLayout(form_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton('Сохранить')
        self.save_button.setIcon(QIcon('ui/resources/icons/save.png'))
        self.save_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton('Отмена')
        self.cancel_button.setObjectName('flat')
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addLayout(buttons_layout)

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

    def accept(self):
        """
        Обработка нажатия кнопки "Сохранить"
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

        # Закрытие диалога с принятием результата
        super().accept()
