from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                            QLineEdit, QComboBox, QMessageBox, QFileDialog)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt, QSize

from controllers import TaskController, ProjectController, DeveloperController, ExportController
from ui.dialogs.task_dialog import TaskDialog

class TasksTab(QWidget):
    """
    Вкладка "Задачи" - управление задачами
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.task_controller = TaskController()
        self.project_controller = ProjectController()
        self.developer_controller = DeveloperController()
        self.export_controller = ExportController()
        self.init_ui()
    
    def init_ui(self):
        """
        Инициализация интерфейса
        """
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Заголовок
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Управление задачами")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        header_layout.addWidget(title_label)
        
        main_layout.addLayout(header_layout)
        
        # Панель поиска и фильтрации
        filter_layout = QHBoxLayout()
        
        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите описание задачи")
        self.search_input.textChanged.connect(self.apply_filters)
        
        project_label = QLabel("Проект:")
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(200)
        self.project_combo.addItem("Все", "")
        self.project_combo.currentIndexChanged.connect(self.apply_filters)
        
        developer_label = QLabel("Разработчик:")
        self.developer_combo = QComboBox()
        self.developer_combo.setMinimumWidth(200)
        self.developer_combo.addItem("Все", "")
        self.developer_combo.currentIndexChanged.connect(self.apply_filters)
        
        status_label = QLabel("Статус:")
        self.status_combo = QComboBox()
        self.status_combo.addItem("Все", "")
        
        # Получение списка статусов
        statuses_result = self.task_controller.get_task_statuses()
        if statuses_result['success']:
            for status in statuses_result['data']:
                self.status_combo.addItem(status, status)
        
        self.status_combo.currentIndexChanged.connect(self.apply_filters)
        
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(project_label)
        filter_layout.addWidget(self.project_combo)
        filter_layout.addWidget(developer_label)
        filter_layout.addWidget(self.developer_combo)
        filter_layout.addWidget(status_label)
        filter_layout.addWidget(self.status_combo)
        filter_layout.addStretch()
        
        main_layout.addLayout(filter_layout)
        
        # Таблица задач
        self.tasks_table = QTableWidget()
        self.tasks_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tasks_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tasks_table.setAlternatingRowColors(True)
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы", "Дата создания"])
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tasks_table.verticalHeader().setVisible(False)
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.doubleClicked.connect(self.edit_item)
        
        main_layout.addWidget(self.tasks_table)
        
        # Панель кнопок
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить")
        self.add_button.setIcon(QIcon('ui/resources/icons/logo.png'))
        self.add_button.clicked.connect(self.add_item)
        
        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setIcon(QIcon('ui/resources/icons/logo.png'))
        self.edit_button.clicked.connect(self.edit_item)
        
        self.delete_button = QPushButton("Удалить")
        self.delete_button.setIcon(QIcon('ui/resources/icons/logo.png'))
        self.delete_button.setObjectName("error")
        self.delete_button.clicked.connect(self.delete_item)
        
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setIcon(QIcon('ui/resources/icons/logo.png'))
        self.refresh_button.clicked.connect(self.refresh_data)
        
        self.export_button = QPushButton("Экспорт")
        self.export_button.setIcon(QIcon('ui/resources/icons/logo.png'))
        self.export_button.clicked.connect(self.export_to_csv)
        
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.export_button)
        
        main_layout.addLayout(buttons_layout)
        
        # Загрузка данных
        self.load_projects_and_developers()
        self.load_tasks()
    
    def load_projects_and_developers(self):
        """
        Загрузка списка проектов и разработчиков для фильтров
        """
        # Загрузка проектов
        projects_result = self.project_controller.get_all_projects()
        if projects_result['success']:
            projects = projects_result['data']


            # Сохранение текущего выбора
            current_project = self.project_combo.currentData()
            
            # Очистка комбобокса
            self.project_combo.clear()
            self.project_combo.addItem("Все", "")
            
            # Добавление проектов
            for project in projects:
                self.project_combo.addItem(project.name, project.id)
            
            # Восстановление выбора
            if current_project:
                index = self.project_combo.findData(current_project)
                if index >= 0:
                    self.project_combo.setCurrentIndex(index)
        
        # Загрузка разработчиков
        developers_result = self.developer_controller.get_all_developers()
        if developers_result['success']:
            developers = developers_result['data']
            
            # Сохранение текущего выбора
            current_developer = self.developer_combo.currentData()
            
            # Очистка комбобокса
            self.developer_combo.clear()
            self.developer_combo.addItem("Все", "")
            
            # Добавление разработчиков
            for developer in developers:
                self.developer_combo.addItem(developer.full_name, developer.id)
            
            # Восстановление выбора
            if current_developer:
                index = self.developer_combo.findData(current_developer)
                if index >= 0:
                    self.developer_combo.setCurrentIndex(index)

    def load_tasks(self):
        """
        Загрузка списка задач
        """
        # Очистка таблицы
        self.tasks_table.setRowCount(0)

        # Получение списка задач
        result = self.task_controller.get_all_tasks()

        print(f"Результат запроса задач: {result}")

        if result['success']:
            tasks = result['data']
            for i, task in enumerate(tasks):
                print(f"Задача {i + 1}: ID={task.id}, Описание={task.description}, Статус={task.status}")

                self.tasks_table.insertRow(i)

                # Заполнение ячеек таблицы
                id_item = QTableWidgetItem(str(task.id))
                project_name = getattr(task, 'project_name', 'Неизвестный проект')
                project_item = QTableWidgetItem(project_name)
                developer_name = getattr(task, 'developer_name', 'Не назначен')
                developer_item = QTableWidgetItem(developer_name)
                description_item = QTableWidgetItem(task.description)
                status_item = QTableWidgetItem(task.status)
                hours_item = QTableWidgetItem(str(task.hours_worked))
                created_at = getattr(task, 'created_at', '')
                created_item = QTableWidgetItem(created_at)

                # Сохраняем ID проекта и разработчика в пользовательских данных
                id_item.setData(Qt.UserRole, task.id)
                project_item.setData(Qt.UserRole, task.project_id)
                developer_item.setData(Qt.UserRole, task.developer_id)

                self.tasks_table.setItem(i, 0, id_item)
                self.tasks_table.setItem(i, 1, project_item)
                self.tasks_table.setItem(i, 2, developer_item)
                self.tasks_table.setItem(i, 3, description_item)
                self.tasks_table.setItem(i, 4, status_item)
                self.tasks_table.setItem(i, 5, hours_item)
                self.tasks_table.setItem(i, 6, created_item)

                # Установка цвета фона в зависимости от статуса
                status_color = {
                    'новая': '#E3F2FD',
                    'в работе': '#FFF8E1',
                    'на проверке': '#F3E5F5',
                    'завершено': '#E8F5E9'
                }.get(task.status, '#FFFFFF')

                # Устанавливаем цвет фона только для созданных ячеек (столбцы 0-6)
                for col in range(7):  # Используем 7 вместо self.tasks_table.columnCount()
                    item = self.tasks_table.item(i, col)
                    if item:  # Проверяем, что элемент существует
                        item.setBackground(QColor(status_color))

    def apply_filters(self):
        """
        Применение фильтров к таблице
        """
        search_text = self.search_input.text().lower()
        project_id = self.project_combo.currentData()
        developer_id = self.developer_combo.currentData()
        status = self.status_combo.currentData()
        
        print(f"Фильтрация: текст='{search_text}', проект ID={project_id}, разработчик ID={developer_id}, статус='{status}'")

        for row in range(self.tasks_table.rowCount()):
            # Получаем данные из строки таблицы
            task_id_item = self.tasks_table.item(row, 0)
            project_item = self.tasks_table.item(row, 1)
            developer_item = self.tasks_table.item(row, 2)
            description = self.tasks_table.item(row, 3).text().lower()
            task_status = self.tasks_table.item(row, 4).text()
            
            # Получаем ID проекта и разработчика из пользовательских данных
            task_project_id = project_item.data(Qt.UserRole)
            task_developer_id = developer_item.data(Qt.UserRole)

            # Проверка соответствия фильтрам
            description_match = search_text in description
            project_match = not project_id or task_project_id == project_id
            developer_match = not developer_id or task_developer_id == developer_id
            status_match = not status or task_status == status
            
            # Отображение/скрытие строки
            should_show = description_match and project_match and developer_match and status_match
            self.tasks_table.setRowHidden(row, not should_show)

            print(f"Задача {task_id_item.text()}: description_match={description_match}, project_match={project_match}, developer_match={developer_match}, status_match={status_match}, показана={should_show}")

    def add_item(self):
        """
        Добавление новой задачи
        """
        dialog = TaskDialog(self)
        if dialog.exec_():
            # Получение данных из диалога
            task_data = {
                'project_id': dialog.project_combo.currentData(),
                'developer_id': dialog.developer_combo.currentData(),
                'description': dialog.description_input.toPlainText(),
                'status': dialog.status_combo.currentText(),
                'hours_worked': float(dialog.hours_input.text() or 0)
            }
            
            # Добавление задачи
            result = self.task_controller.create_task(task_data)
            
            if result['success']:
                QMessageBox.information(self, "Успех", "Задача успешно добавлена")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def edit_item(self):
        """
        Редактирование выбранной задачи
        """
        # Получение выбранной строки
        selected_rows = self.tasks_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для редактирования")
            return
        
        # Получение ID выбранной задачи
        row = selected_rows[0].row()
        task_id = int(self.tasks_table.item(row, 0).text())
        
        # Получение данных задачи
        result = self.task_controller.get_task_by_id(task_id)
        
        if result['success']:
            task = result['data']
            
            # Открытие диалога редактирования
            dialog = TaskDialog(self, task)
            if dialog.exec_():
                # Получение данных из диалога
                task_data = {
                    'project_id': dialog.project_combo.currentData(),
                    'developer_id': dialog.developer_combo.currentData(),
                    'description': dialog.description_input.toPlainText(),
                    'status': dialog.status_combo.currentText(),
                    'hours_worked': float(dialog.hours_input.text() or 0)
                }
                
                # Обновление задачи
                update_result = self.task_controller.update_task(task_id, task_data)
                
                if update_result['success']:
                    QMessageBox.information(self, "Успех", "Задача успешно обновлена")
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "Ошибка", update_result['error_message'])
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def delete_item(self):
        """
        Удаление выбранной задачи
        """
        # Получение выбранной строки
        selected_rows = self.tasks_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для удаления")
            return
        
        # Получение ID выбранной задачи
        row = selected_rows[0].row()
        task_id = int(self.tasks_table.item(row, 0).text())
        task_description = self.tasks_table.item(row, 3).text()
        
        # Подтверждение удаления
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить задачу '{task_description}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Удаление задачи
            result = self.task_controller.delete_task(task_id)
            
            if result['success']:
                QMessageBox.information(self, "Успех", "Задача успешно удалена")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def refresh_data(self):
        """
        Обновление данных в таблице
        """
        self.load_projects_and_developers()
        self.load_tasks()
        self.apply_filters()
    
    def export_to_csv(self):
        """
        Экспорт данных в CSV
        """
        # Открытие диалога сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            # Подготовка данных для экспорта
            headers = ["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы", "Дата создания"]
            data = []
            
            for row in range(self.tasks_table.rowCount()):
                if not self.tasks_table.isRowHidden(row):
                    row_data = []
                    for col in range(self.tasks_table.columnCount()):
                        row_data.append(self.tasks_table.item(row, col).text())
                    data.append(row_data)
            
            # Экспорт в CSV
            result = self.export_controller.export_data_to_csv(data, headers, file_path)
            
            if result['success']:
                QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def export_to_excel(self):
        """
        Экспорт данных в Excel
        """
        # Открытие диалога сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить Excel", "", "Excel Files (*.xlsx);;All Files (*)"
        )
        
        if file_path:
            # Подготовка данных для экспорта
            headers = ["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы", "Дата создания"]
            data = []
            
            for row in range(self.tasks_table.rowCount()):
                if not self.tasks_table.isRowHidden(row):
                    row_data = []
                    for col in range(self.tasks_table.columnCount()):
                        row_data.append(self.tasks_table.item(row, col).text())
                    data.append(row_data)
            
            # Экспорт в Excel
            result = self.export_controller.export_data_to_excel(data, headers, file_path, "Задачи")
            
            if result['success']:
                QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
