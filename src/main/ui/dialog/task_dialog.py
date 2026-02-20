from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QFormLayout, QMessageBox, QComboBox, 
                            QTextEdit, QDoubleSpinBox)
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator
from PyQt5.QtCore import Qt

from src.main.service.controllers import TaskController, ProjectController, DeveloperController

class TaskDialog(QDialog):
    """
    Диалог добавления/редактирования задачи
    """
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.task_controller = TaskController()
        self.project_controller = ProjectController()
        self.developer_controller = DeveloperController()
        self.init_ui()
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Настройка окна
        self.setWindowTitle('Задача' if not self.task else 'Редактирование задачи')
        self.setWindowIcon(QIcon('ui/resources/icons/task.png'))
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
        self.project_combo = QComboBox()
        self.load_projects()
        
        self.developer_combo = QComboBox()
        self.load_developers()
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Введите описание задачи')
        self.description_input.setMinimumHeight(100)
        
        self.status_combo = QComboBox()
        
        # Получение списка статусов
        statuses_result = self.task_controller.get_task_statuses()
        if statuses_result['success']:
            for status in statuses_result['data']:
                self.status_combo.addItem(status, status)
        
        self.hours_input = QLineEdit()
        self.hours_input.setPlaceholderText('Введите количество часов')
        self.hours_input.setValidator(QDoubleValidator(0, 1000, 2))
        
        form_layout.addRow('Проект*:', self.project_combo)
        form_layout.addRow('Разработчик*:', self.developer_combo)
        form_layout.addRow('Описание*:', self.description_input)
        form_layout.addRow('Статус*:', self.status_combo)
        form_layout.addRow('Часы:', self.hours_input)
        
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
        
        # Заполнение полей, если редактируем существующую задачу
        if self.task:
            # Установка проекта
            project_index = self.project_combo.findData(self.task.project_id)
            if project_index >= 0:
                self.project_combo.setCurrentIndex(project_index)
            
            # Установка разработчика
            developer_index = self.developer_combo.findData(self.task.developer_id)
            if developer_index >= 0:
                self.developer_combo.setCurrentIndex(developer_index)
            
            self.description_input.setText(self.task.description)
            
            # Установка статуса
            status_index = self.status_combo.findText(self.task.status)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
            
            self.hours_input.setText(str(self.task.hours_worked))
    
    def load_projects(self):
        """
        Загрузка списка проектов
        """
        # Получение списка проектов
        result = self.project_controller.get_all_projects()
        
        if result['success']:
            projects = result['data']
            
            # Добавление проектов в комбобокс
            for project in projects:
                self.project_combo.addItem(project.name, project.id)
    
    def load_developers(self):
        """
        Загрузка списка разработчиков
        """
        # Получение списка разработчиков
        result = self.developer_controller.get_all_developers()
        
        if result['success']:
            developers = result['data']
            
            # Добавление разработчиков в комбобокс
            for developer in developers:
                self.developer_combo.addItem(developer.full_name, developer.id)
    
    def accept(self):
        """
        Обработка нажатия кнопки "Сохранить"
        """
        # Проверка заполнения обязательных полей
        if not self.description_input.toPlainText():
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, заполните описание задачи')
            return
        
        if self.project_combo.currentIndex() < 0:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите проект')
            return
        
        if self.developer_combo.currentIndex() < 0:
            QMessageBox.warning(self, 'Предупреждение', 'Пожалуйста, выберите разработчика')
            return
        
        # Проверка корректности часов
        if self.hours_input.text():
            try:
                hours = float(self.hours_input.text())
                if hours < 0:
                    QMessageBox.warning(self, 'Предупреждение', 'Часы должны быть положительным числом')
                    return
            except ValueError:
                QMessageBox.warning(self, 'Предупреждение', 'Часы должны быть числом')
                return
        
        # Закрытие диалога с принятием результата
        super().accept()
