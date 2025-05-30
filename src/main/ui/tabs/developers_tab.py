from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                            QLineEdit, QComboBox, QMessageBox, QFileDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from src.main.service.controllers import DeveloperController, ExportController
from src.main.ui.dialog.developer_dialog import DeveloperDialog

class DevelopersTab(QWidget):
    """
    Вкладка "Разработчики" - управление разработчиками
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
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
        
        title_label = QLabel("Управление разработчиками")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        header_layout.addWidget(title_label)
        
        main_layout.addLayout(header_layout)
        
        # Панель поиска и фильтрации
        filter_layout = QHBoxLayout()
        
        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите имя разработчика")
        self.search_input.textChanged.connect(self.apply_filters)
        
        position_label = QLabel("Должность:")
        self.position_combo = QComboBox()
        self.position_combo.addItem("Все", "")

        # Получение списка должностей
        positions_result = self.developer_controller.get_developer_positions()
        if positions_result['success']:
            for position in positions_result['data']:
                self.position_combo.addItem(position, position)
        
        self.position_combo.currentIndexChanged.connect(self.apply_filters)
        
        filter_layout.addWidget(search_label)
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(position_label)
        filter_layout.addWidget(self.position_combo)
        filter_layout.addStretch()
        
        main_layout.addLayout(filter_layout)
        
        # Таблица разработчиков
        self.developers_table = QTableWidget()
        self.developers_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.developers_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.developers_table.setAlternatingRowColors(True)
        self.developers_table.setColumnCount(4)
        self.developers_table.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Ставка в час"])
        self.developers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.developers_table.verticalHeader().setVisible(False)
        self.developers_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.developers_table.doubleClicked.connect(self.edit_item)
        
        main_layout.addWidget(self.developers_table)
        
        # Панель кнопок
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить")
        self.add_button.setIcon(QIcon('ui/resources/icons/add.png'))
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
        self.load_developers()
    
    def load_developers(self):
        """
        Загрузка списка разработчиков
        """
        # Очистка таблицы
        self.developers_table.setRowCount(0)
        
        # Получение списка разработчиков
        result = self.developer_controller.get_all_developers()
        
        if result['success']:
            developers = result['data']
            
            # Заполнение таблицы
            for row, developer in enumerate(developers):
                self.developers_table.insertRow(row)
                
                id_item = QTableWidgetItem(str(developer.id))
                name_item = QTableWidgetItem(developer.full_name)
                position_item = QTableWidgetItem(developer.position)
                rate_item = QTableWidgetItem(str(developer.hourly_rate))
                
                self.developers_table.setItem(row, 0, id_item)
                self.developers_table.setItem(row, 1, name_item)
                self.developers_table.setItem(row, 2, position_item)
                self.developers_table.setItem(row, 3, rate_item)
    
    def apply_filters(self):
        """
        Применение фильтров к таблице
        """
        search_text = self.search_input.text().lower()
        position = self.position_combo.currentData()
        
        for row in range(self.developers_table.rowCount()):
            name = self.developers_table.item(row, 1).text().lower()
            dev_position = self.developers_table.item(row, 2).text()
            
            # Проверка соответствия фильтрам
            name_match = search_text in name
            position_match = not position or dev_position == position
            
            # Отображение/скрытие строки
            self.developers_table.setRowHidden(row, not (name_match and position_match))
    
    def add_item(self):
        """
        Добавление нового разработчика
        """
        dialog = DeveloperDialog(self)
        if dialog.exec_():
            # Получение данных из диалога
            developer_data = {
                'full_name': dialog.name_input.text(),
                'position': dialog.position_combo.currentText(),
                'hourly_rate': float(dialog.rate_input.text())
            }
            
            # Добавление разработчика
            result = self.developer_controller.create_developer(developer_data)
            
            if result['success']:
                QMessageBox.information(self, "Успех", "Разработчик успешно добавлен")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def edit_item(self):
        """
        Редактирование выбранного разработчика
        """
        # Получение выбранной строки
        selected_rows = self.developers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите разработчика для редактирования")
            return
        
        # Получение ID выбранного разработчика
        row = selected_rows[0].row()
        developer_id = int(self.developers_table.item(row, 0).text())
        
        # Получение данных разработчика
        result = self.developer_controller.get_developer_by_id(developer_id)
        
        if result['success']:
            developer = result['data']
            
            # Открытие диалога редактирования
            dialog = DeveloperDialog(self, developer)
            if dialog.exec_():
                # Получение данных из диалога
                developer_data = {
                    'full_name': dialog.name_input.text(),
                    'position': dialog.position_combo.currentText(),
                    'hourly_rate': float(dialog.rate_input.text())
                }
                
                # Обновление разработчика
                update_result = self.developer_controller.update_developer(developer_id, developer_data)
                
                if update_result['success']:
                    QMessageBox.information(self, "Успех", "Разработчик успешно обновлен")
                    self.refresh_data()
                else:
                    QMessageBox.critical(self, "Ошибка", update_result['error_message'])
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def delete_item(self):
        """
        Удаление выбранного разработчика
        """
        # Получение выбранной строки
        selected_rows = self.developers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите разработчика для удаления")
            return
        
        # Получение ID выбранного разработчика
        row = selected_rows[0].row()
        developer_id = int(self.developers_table.item(row, 0).text())
        developer_name = self.developers_table.item(row, 1).text()
        
        # Подтверждение удаления
        reply = QMessageBox.question(
            self, "Подтверждение", 
            f"Вы уверены, что хотите удалить разработчика '{developer_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Удаление разработчика
            result = self.developer_controller.delete_developer(developer_id)
            
            if result['success']:
                QMessageBox.information(self, "Успех", "Разработчик успешно удален")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def refresh_data(self):
        """
        Обновление данных в таблице
        """
        self.load_developers()
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
            headers = ["ID", "ФИО", "Должность", "Ставка в час"]
            data = []
            
            for row in range(self.developers_table.rowCount()):
                if not self.developers_table.isRowHidden(row):
                    row_data = []
                    for col in range(self.developers_table.columnCount()):
                        row_data.append(self.developers_table.item(row, col).text())
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
            headers = ["ID", "ФИО", "Должность", "Ставка в час"]
            data = []
            
            for row in range(self.developers_table.rowCount()):
                if not self.developers_table.isRowHidden(row):
                    row_data = []
                    for col in range(self.developers_table.columnCount()):
                        row_data.append(self.developers_table.item(row, col).text())
                    data.append(row_data)
            
            # Экспорт в Excel
            result = self.export_controller.export_data_to_excel(data, headers, file_path, "Разработчики")
            
            if result['success']:
                QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
