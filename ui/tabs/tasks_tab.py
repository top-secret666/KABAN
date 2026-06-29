from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QLineEdit, QComboBox, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt

from controllers import TaskController, ProjectController, DeveloperController, ExportController
from ui.dialogs.task_dialog import TaskDialog
from ui.widgets.tab_page import TabPage
from ui.widgets.page_header import FilterPanel
from ui.resources.icon_helper import get_icon
from ui.resources.table_helper import configure_table, apply_task_row_colors, unhide_all_rows
from ui.resources.combo_helper import reload_combo


class TasksTab(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.task_controller = TaskController()
        self.project_controller = ProjectController()
        self.developer_controller = DeveloperController()
        self.export_controller = ExportController()
        self.init_ui()

        if self.user.role == 'developer':
            if hasattr(self, 'developer_label'):
                self.developer_label.setVisible(False)
            if hasattr(self, 'developer_combo'):
                self.developer_combo.setVisible(False)


    def init_ui(self):
        page = TabPage('Задачи', 'Управление задачами и статусами')
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(page)
        main_layout = page.content_layout

        filter_panel = FilterPanel()
        fl = filter_panel.layout()

        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите описание задачи")
        self.search_input.setMinimumWidth(200)
        self.search_input.textChanged.connect(self.apply_filters)

        project_label = QLabel("Проект:")
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(180)
        self.project_combo.addItem("Все", "")
        self.project_combo.currentIndexChanged.connect(self.apply_filters)
        self.developer_label = QLabel("Разработчик:")
        self.developer_combo = QComboBox()
        self.developer_combo.setMinimumWidth(180)
        self.developer_combo.addItem("Все", "")
        self.developer_combo.currentIndexChanged.connect(self.apply_filters)

        status_label = QLabel("Статус:")
        self.status_combo = QComboBox()
        self.status_combo.addItem("Все", "")
        statuses_result = self.task_controller.get_task_statuses()
        if statuses_result['success']:
            for status in statuses_result['data']:
                self.status_combo.addItem(status, status)
        self.status_combo.currentIndexChanged.connect(self.apply_filters)

        for w in [search_label, self.search_input, project_label, self.project_combo,
                  self.developer_label, self.developer_combo, status_label, self.status_combo]:
            fl.addWidget(w)
        fl.addStretch()
        main_layout.addWidget(filter_panel)

        self.tasks_table = QTableWidget()
        configure_table(self.tasks_table)
        self.tasks_table.setProperty('task_status_col', 4)
        self.tasks_table.setProperty('task_num_cols', 7)
        self.tasks_table.setColumnCount(7)
        self.tasks_table.setHorizontalHeaderLabels(["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы", "Дата создания"])
        self.tasks_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.doubleClicked.connect(self.edit_item)
        
        main_layout.addWidget(self.tasks_table)

        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.add_button.setIcon(get_icon('add'))
        self.add_button.clicked.connect(self.add_item)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.setIcon(get_icon('edit'))
        self.edit_button.clicked.connect(self.edit_item)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setIcon(get_icon('delete'))
        self.delete_button.setObjectName("error")
        self.delete_button.clicked.connect(self.delete_item)

        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setIcon(get_icon('refresh'))
        self.refresh_button.clicked.connect(self.refresh_data)

        self.export_button = QPushButton("Экспорт")
        self.export_button.setIcon(get_icon('export'))
        self.export_button.clicked.connect(self.export_to_csv)
        
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.export_button)
        
        main_layout.addLayout(buttons_layout)

        self.load_projects_and_developers()
        self.load_tasks()

    def load_projects_and_developers(self):
        if self.user and self.user.role == 'developer':
            developer_result = self.developer_controller.get_developer_by_user_id(self.user.id)
            if developer_result['success'] and developer_result['data']:
                developer = developer_result['data']
                result = self.project_controller.get_projects_by_developer(developer.id)
                projects = result['data'] if result.get('success') else []
            else:
                projects = []
            reload_combo(
                self.project_combo,
                [(p.name, p.id) for p in projects],
                first_label='Все',
                first_data='',
            )
        else:
            projects_result = self.project_controller.get_all_projects()
            if projects_result['success']:
                projects = projects_result['data']
                reload_combo(
                    self.project_combo,
                    [(p.name, p.id) for p in projects],
                    first_label='Все',
                    first_data='',
                )

        if self.user.role != 'developer':
            developers_result = self.developer_controller.get_all_developers()
            if developers_result['success']:
                developers = developers_result['data']
                reload_combo(
                    self.developer_combo,
                    [(d.full_name, d.id) for d in developers],
                    first_label='Все',
                    first_data='',
                )

    def load_tasks(self):
        self.tasks_table.setRowCount(0)

        try:
            if self.user.role == 'developer':
                developer_result = self.developer_controller.get_developer_by_user_id(self.user.id)
                if developer_result['success'] and developer_result['data']:
                    result = self.task_controller.get_tasks_by_developer(developer_result['data'].id)
                else:
                    result = {'success': True, 'data': []}
            else:
                result = self.task_controller.get_all_tasks()

            if result['success']:
                for i, task in enumerate(result['data']):
                    self.tasks_table.insertRow(i)

                    id_item = QTableWidgetItem(str(task.id))
                    project_item = QTableWidgetItem(getattr(task, 'project_name', None) or 'Неизвестный проект')
                    developer_item = QTableWidgetItem(getattr(task, 'developer_name', None) or 'Не назначен')
                    description_item = QTableWidgetItem(task.description or '')
                    status_item = QTableWidgetItem(task.status or '')
                    hours_item = QTableWidgetItem(str(task.hours_worked or 0))
                    created_item = QTableWidgetItem(str(getattr(task, 'created_at', None) or ''))

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

            apply_task_row_colors(self.tasks_table, status_col=4, num_cols=7)
            unhide_all_rows(self.tasks_table)
        except Exception:
            pass

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        project_id = self.project_combo.currentData()
        developer_id = self.developer_combo.currentData()
        status = self.status_combo.currentData()

        for row in range(self.tasks_table.rowCount()):
            project_item = self.tasks_table.item(row, 1)
            developer_item = self.tasks_table.item(row, 2)
            description = self.tasks_table.item(row, 3).text().lower()
            task_status = self.tasks_table.item(row, 4).text()
            task_project_id = project_item.data(Qt.UserRole)
            task_developer_id = developer_item.data(Qt.UserRole)

            should_show = (
                search_text in description
                and (not project_id or task_project_id == project_id)
                and (not developer_id or task_developer_id == developer_id)
                and (not status or task_status == status)
            )
            self.tasks_table.setRowHidden(row, not should_show)

    def add_item(self):
        dialog = TaskDialog(self)
        if dialog.exec_():
            task_data = {
                'project_id': dialog.project_combo.currentData(),
                'developer_id': dialog.developer_combo.currentData(),
                'description': dialog.description_input.toPlainText(),
                'status': dialog.status_combo.currentText(),
                'hours_worked': float(dialog.hours_input.text() or 0),
            }
            result = self.task_controller.create_task(task_data)
            if result['success']:
                QMessageBox.information(self, "Успех", "Задача успешно добавлена")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])

    def edit_item(self):
        selected_rows = self.tasks_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для редактирования")
            return

        row = selected_rows[0].row()
        task_id = int(self.tasks_table.item(row, 0).text())
        result = self.task_controller.get_task_by_id(task_id)

        if result['success']:
            dialog = TaskDialog(self, result['data'])
            if dialog.exec_():
                task_data = {
                    'project_id': dialog.project_combo.currentData(),
                    'developer_id': dialog.developer_combo.currentData(),
                    'description': dialog.description_input.toPlainText(),
                    'status': dialog.status_combo.currentText(),
                    'hours_worked': float(dialog.hours_input.text() or 0),
                }
                update_result = self.task_controller.update_task(task_id, task_data)
                if update_result['success']:
                    QMessageBox.information(self, "Успех", "Задача успешно обновлена")
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "Ошибка", update_result['error_message'])
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])

    def delete_item(self):
        selected_rows = self.tasks_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите задачу для удаления")
            return

        row = selected_rows[0].row()
        task_id = int(self.tasks_table.item(row, 0).text())
        task_description = self.tasks_table.item(row, 3).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить задачу '{task_description}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.task_controller.delete_task(task_id)
            if result['success']:
                QMessageBox.information(self, "Успех", "Задача успешно удалена")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])

    def refresh_data(self):
        self.load_tasks()
        self.load_projects_and_developers()
        self.apply_filters()

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        headers = ["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы", "Дата создания"]
        data = []
        for row in range(self.tasks_table.rowCount()):
            if not self.tasks_table.isRowHidden(row):
                data.append([self.tasks_table.item(row, col).text() for col in range(self.tasks_table.columnCount())])

        result = self.export_controller.export_data_to_csv(data, headers, file_path)
        if result['success']:
            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])

    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить Excel", "", "Excel Files (*.xlsx);;All Files (*)"
        )
        if not file_path:
            return

        headers = ["ID", "Проект", "Разработчик", "Описание", "Статус", "Часы", "Дата создания"]
        data = []
        for row in range(self.tasks_table.rowCount()):
            if not self.tasks_table.isRowHidden(row):
                data.append([self.tasks_table.item(row, col).text() for col in range(self.tasks_table.columnCount())])

        result = self.export_controller.export_data_to_excel(data, headers, file_path, "Задачи")
        if result['success']:
            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
