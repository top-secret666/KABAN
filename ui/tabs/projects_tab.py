from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                             QLineEdit, QComboBox, QMessageBox, QFileDialog, QDateEdit, QDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QDate

from controllers import ProjectController, ExportController
from models import DBManager
from ui.dialogs.new_project_dialog import NewProjectDialog
from ui.dialogs.project_dialog import ProjectDialog


class ProjectsTab(QWidget):
    """
    Вкладка "Проекты" - управление проектами
    """

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.project_controller = ProjectController()
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

        title_label = QLabel("Управление проектами")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        header_layout.addWidget(title_label)

        main_layout.addLayout(header_layout)

        # Панель поиска и фильтрации
        filter_layout = QHBoxLayout()

        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите название проекта или клиента")
        self.search_input.textChanged.connect(self.apply_filters)

        client_label = QLabel("Клиент:")
        self.client_combo = QComboBox()
        self.client_combo.setMinimumWidth(200)
        self.client_combo.addItem("Все", "")

        date_label = QLabel("Дедлайн:")
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-12))
        self.date_from.dateChanged.connect(self.apply_filters)

        date_to_label = QLabel("до:")
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate().addMonths(12))
        self.date_to.dateChanged.connect(self.apply_filters)

        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(client_label)
        filter_layout.addWidget(self.client_combo)
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(date_to_label)
        filter_layout.addWidget(self.date_to)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

        # Таблица проектов
        self.projects_table = QTableWidget()
        self.projects_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.projects_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.projects_table.setAlternatingRowColors(True)
        self.projects_table.setColumnCount(6)
        self.projects_table.setHorizontalHeaderLabels(["ID", "Название", "Клиент", "Дедлайн", "Бюджет", "Статус"])
        self.projects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.projects_table.verticalHeader().setVisible(False)
        self.projects_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.projects_table.doubleClicked.connect(self.edit_item)

        main_layout.addWidget(self.projects_table)

        # Панель кнопок
        buttons_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.setIcon(QIcon('ui/resources/icons/add.png'))
        print("Подключаем обработчик к кнопке Добавить")
        self.add_button.clicked.connect(self.add_item)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setIcon(QIcon('ui/resources/icons/edit.png'))
        self.edit_button.clicked.connect(self.edit_item)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setIcon(QIcon('ui/resources/icons/delete.png'))
        self.delete_button.setObjectName("error")
        self.delete_button.clicked.connect(self.delete_item)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setIcon(QIcon('ui/resources/icons/refresh.png'))
        self.refresh_button.clicked.connect(self.refresh_data)

        self.export_button = QPushButton("Экспорт")
        self.export_button.setIcon(QIcon('ui/resources/icons/export.png'))
        self.export_button.clicked.connect(self.export_to_csv)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.export_button)

        main_layout.addLayout(buttons_layout)

        # Загрузка данных
        self.load_projects()

    def load_projects(self):
        """
        Загрузка списка проектов
        """
        # Очистка таблицы
        self.projects_table.setRowCount(0)

        # Получение списка проектов в зависимости от роли пользователя
        if self.user.role == 'developer':
            # Для разработчика показываем только его проекты
            # Сначала получаем ID разработчика по ID пользователя
            from controllers import DeveloperController
            developer_controller = DeveloperController()

            developer_result = developer_controller.get_developer_by_user_id(self.user.id)

            if developer_result['success'] and developer_result['data']:
                developer = developer_result['data']
                print(f"Найден разработчик для пользователя {self.user.id}: {developer.full_name} (ID: {developer.id})")
                # Теперь используем ID разработчика для получения проектов
                result = self.project_controller.get_projects_by_developer(developer.id)
            else:
                # Если разработчик не найден, показываем пустой список
                print(f"Разработчик для пользователя {self.user.id} не найден")
                result = {'success': True, 'data': []}
        else:
            # Для менеджеров и администраторов показываем все проекты
            result = self.project_controller.get_all_projects()

        print(f"Результат запроса проектов: {result}")

        if result['success']:
            projects = result['data']
            print(f"Количество проектов: {len(projects)}")
            for project in projects:
                print(f"ID: {project.id}, Название: {project.name}, Клиент: {project.client}, Бюджет: {project.budget}")

            # Заполнение таблицы
            for row, project in enumerate(projects):
                self.projects_table.insertRow(row)

                id_item = QTableWidgetItem(str(project.id))
                name_item = QTableWidgetItem(project.name)
                client_item = QTableWidgetItem(project.client)
                deadline_item = QTableWidgetItem(project.deadline if project.deadline else "")
                budget_item = QTableWidgetItem(str(project.budget))
                print(f"Проект {project.id} статус: {project.status}")
                status_item = QTableWidgetItem(project.status)

                self.projects_table.setItem(row, 0, id_item)
                self.projects_table.setItem(row, 1, name_item)
                self.projects_table.setItem(row, 2, client_item)
                self.projects_table.setItem(row, 3, deadline_item)
                self.projects_table.setItem(row, 4, budget_item)
                self.projects_table.setItem(row, 5, status_item)

            # Обновление списка клиентов для фильтра
            self.update_client_filter(projects)

    def update_client_filter(self, projects):
        """
        Обновление списка клиентов для фильтра
        """
        # Сохранение текущего выбора
        current_client = self.client_combo.currentData()

        # Очистка комбобокса
        self.client_combo.clear()
        self.client_combo.addItem("Все", "")

        # Получение уникальных клиентов
        clients = set()
        for project in projects:
            if project.client:
                clients.add(project.client)

        # Добавление клиентов в комбобокс
        for client in sorted(clients):
            self.client_combo.addItem(client, client)

        # Восстановление выбора
        if current_client:
            index = self.client_combo.findData(current_client)
            if index >= 0:
                self.client_combo.setCurrentIndex(index)

    def apply_filters(self):
        """
        Применение фильтров к таблице
        """
        print("Применение фильтров к проектам")
        search_text = self.search_input.text().lower()
        client = self.client_combo.currentData()

        # Получаем объекты QDate вместо строк
        date_from_obj = self.date_from.date()
        date_to_obj = self.date_to.date()

        for row in range(self.projects_table.rowCount()):
            name = self.projects_table.item(row, 1).text().lower()
            proj_client = self.projects_table.item(row, 2).text()
            deadline = self.projects_table.item(row, 3).text()

            # Проверка соответствия фильтрам
            name_match = search_text in name.lower() or search_text in proj_client.lower()
            client_match = not client or proj_client == client

            # Проверка даты
            date_match = True
            if deadline:
                try:
                    # Преобразуем строку дедлайна в объект QDate
                    deadline_date = QDate.fromString(deadline, "yyyy-MM-dd")
                    if deadline_date.isValid():
                        date_match = date_from_obj <= deadline_date <= date_to_obj
                        print(
                            f"Дата проекта: {deadline}, диапазон: {date_from_obj.toString('yyyy-MM-dd')} - {date_to_obj.toString('yyyy-MM-dd')}, результат: {date_match}")
                except Exception as e:
                    print(f"Ошибка при проверке даты: {e}")
                    date_match = True  # В случае ошибки не фильтруем по дате

            # Отображение/скрытие строки
            should_show = name_match and client_match and date_match
            self.projects_table.setRowHidden(row, not should_show)
            print(f"Проект {row} {'показан' if should_show else 'скрыт'}")

        # Подсчет видимых строк после применения всех фильтров
        visible_rows = 0
        for row in range(self.projects_table.rowCount()):
            if not self.projects_table.isRowHidden(row):
                visible_rows += 1

        print(f"Видимых проектов после фильтрации: {visible_rows}")

    def add_item(self):
        """
        Добавление нового проекта
        """
        try:
            # Используем новый диалог
            dialog = NewProjectDialog(self)

            # Отображаем диалог и ждем результат
            if dialog.exec_():
                # Получение данных из диалога
                project_data = {
                    'name': dialog.name_input.text(),
                    'client': dialog.client_input.text(),
                    'deadline': dialog.deadline_input.date().toString("yyyy-MM-dd"),
                    'budget': float(dialog.budget_input.text())
                }

                # Добавление проекта
                result = self.project_controller.create_project(project_data)

                if result['success']:
                    QMessageBox.information(self, "Успех", "Проект успешно добавлен")
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "Ошибка", result['error_message'])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при создании диалога: {str(e)}")
            import traceback
            traceback.print_exc()

    def on_dialog_rejected(self):
        """
        Обработка отклонения диалога
        """
        print("Диалог отклонен")

    def edit_item(self):
        """
        Редактирование выбранного проекта
        """
        try:
            # Получение выбранной строки
            selected_rows = self.projects_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "Предупреждение", "Выберите проект для редактирования")
                return

            # Получение ID выбранного проекта
            row = selected_rows[0].row()
            project_id = int(self.projects_table.item(row, 0).text())

            # Получение проекта
            result = self.project_controller.get_project_by_id(project_id)

            if result['success']:
                project = result['data']

                # Используем новый диалог
                dialog = NewProjectDialog(self, project)

                # Отображаем диалог и ждем результат
                if dialog.exec_():
                    # Получение данных из диалога
                    project_data = {
                        'name': dialog.name_input.text(),
                        'client': dialog.client_input.text(),
                        'deadline': dialog.deadline_input.date().toString("yyyy-MM-dd"),
                        'budget': float(dialog.budget_input.text())
                    }

                    # Обновление проекта
                    update_result = self.project_controller.update_project(project_id, project_data)

                    if update_result['success']:
                        QMessageBox.information(self, "Успех", "Проект успешно обновлен")
                        self.refresh_data()
                    else:
                        QMessageBox.critical(self, "Ошибка", update_result['error_message'])
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании: {str(e)}")
            import traceback
            traceback.print_exc()

    def delete_item(self):
        """
        Удаление выбранного проекта
        """
        # Получение выбранной строки
        selected_rows = self.projects_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите проект для удаления")
            return

        # Получение ID выбранного проекта
        row = selected_rows[0].row()
        project_id = int(self.projects_table.item(row, 0).text())
        project_name = self.projects_table.item(row, 1).text()

        # Подтверждение удаления
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить проект '{project_name}'?\nВсе связанные задачи также будут удалены.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Удаление проекта
            result = self.project_controller.delete_project(project_id)

            if result['success']:
                QMessageBox.information(self, "Успех", "Проект успешно удален")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])

    def refresh_data(self):
        """
        Обновление данных в таблице
        """
        self.load_projects()
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
            headers = ["ID", "Название", "Клиент", "Дедлайн", "Бюджет", "Статус"]
            data = []

            for row in range(self.projects_table.rowCount()):
                if not self.projects_table.isRowHidden(row):
                    row_data = []
                    for col in range(self.projects_table.columnCount()):
                        row_data.append(self.projects_table.item(row, col).text())
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
            headers = ["ID", "Название", "Клиент", "Дедлайн", "Бюджет", "Статус"]
            data = []

            for row in range(self.projects_table.rowCount()):
                if not self.projects_table.isRowHidden(row):
                    row_data = []
                    for col in range(self.projects_table.columnCount()):
                        row_data.append(self.projects_table.item(row, col).text())
                    data.append(row_data)

            # Экспорт в Excel
            result = self.export_controller.export_data_to_excel(data, headers, file_path, "Проекты")

            if result['success']:
                QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
                QMessageBox.critical(self, "Ошибка", result['error_message'])
