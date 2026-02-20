from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFormLayout, QMessageBox, QComboBox, QDoubleSpinBox)
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator
from PyQt5.QtCore import Qt

from controllers import DeveloperController

class DeveloperDialog(QDialog):
    """
    Диалог добавления/редактирования разработчика
    """

    def __init__(self, parent=None, developer=None):
        print("Инициализация DeveloperDialog")
        super().__init__(parent)
        self.developer = developer
        self.developer_controller = DeveloperController()
        print("Контроллер создан")
        self.init_ui()
        print("UI инициализирован")
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('Разработчик' if not self.developer else 'Редактирование разработчика')
        self.setWindowIcon(QIcon('ui/resources/icons/developer.png'))
        self.setMinimumWidth(400)
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
        self.name_input.setPlaceholderText('Введите ФИО разработчика')
        
        self.position_combo = QComboBox()
        
        # Получение списка должностей
        positions_result = self.developer_controller.get_developer_positions()
        if positions_result['success']:
            for position in positions_result['data']:
                self.position_combo.addItem(position, position)
        
        self.rate_input = QLineEdit()
        self.rate_input.setPlaceholderText('Введите ставку в час')
        self.rate_input.setValidator(QDoubleValidator(0, 100000, 2))
        
        form_layout.addRow('ФИО*:', self.name_input)
        form_layout.addRow('Должность*:', self.position_combo)
        form_layout.addRow('Ставка в час*:', self.rate_input)
        
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
        
        # Заполнение полей, если редактируем существующего разработчика
        if self.developer:
            self.name_input.setText(self.developer.full_name)
            
            # Установка должности
            index = self.position_combo.findData(self.developer.position)
            if index >= 0:
                self.position_combo.setCurrentIndex(index)
            
            self.rate_input.setText(str(self.developer.hourly_rate))
    
    def accept(self):
        """
        Обработка нажатия кнопки "Сохранить"
        """
        # Проверка заполнения обязательных полей
        if not self.name_input.text() or not self.rate_input.text():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, заполните все обязательные поля')
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
        
        # Закрытие диалога с принятием результата
        super().accept()
