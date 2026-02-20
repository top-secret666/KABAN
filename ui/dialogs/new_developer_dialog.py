from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFormLayout, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt

from controllers import DeveloperController


class NewDeveloperDialog(QDialog):
    """
    Упрощенный диалог добавления/редактирования разработчика
    """

    def __init__(self, parent=None, developer=None):
        super().__init__(parent)
        self.developer = developer
        self.developer_controller = DeveloperController()

        # Настройка окна
        self.setWindowTitle('Разработчик' if not self.developer else 'Редактирование разработчика')
        self.setMinimumWidth(400)
        self.setMinimumHeight(250)

        # Основной layout
        layout = QVBoxLayout(self)

        # Форма
        form_layout = QFormLayout()

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите ФИО разработчика')

        self.position_combo = QComboBox()
        positions_result = self.developer_controller.get_developer_positions()
        if positions_result['success']:
            for position in positions_result['data']:
                self.position_combo.addItem(position, position)

        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText('Введите ставку в час')

        form_layout.addRow('ФИО*:', self.name_input)
        form_layout.addRow('Должность*:', self.position_combo)
        form_layout.addRow('Ставка в час*:', self.rate_input)

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

        # Заполнение полей, если редактируем существующего разработчика
        if self.developer:
            self.name_input.setText(self.developer.full_name)

            # Установка должности
            index = self.position_combo.findData(self.developer.position)
            if index >= 0:
                self.position_combo.setCurrentIndex(index)

            self.rate_input.setText(str(self.developer.hourly_rate))

    def validate_and_accept(self):
        """
        Проверка данных перед закрытием диалога
        """
        # Проверка заполнения обязательных полей
        if not self.name_input.text():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, заполните ФИО разработчика')
            return

        if not self.rate_input.text():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, укажите ставку в час')
            return

        # Проверка корректности ставки
        try:
            rate = float(self.rate_input.text())
            if rate <= 0:
                QMessageBox.warning(self, 'Предупреждение', 'Ставка должна быть положительным числом')
                return
        except ValueError:
            QMessageBox.warning(self, 'Предупреждение', 'Ставка должна быть числом')
            return

        # Если все проверки пройдены, закрываем диалог с принятием результата
        self.accept()
