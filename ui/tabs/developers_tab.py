from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                            QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                            QLineEdit, QComboBox, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QSize

from controllers import DeveloperController, ExportController
from ui.dialogs.new_developer_dialog import NewDeveloperDialog
from ui.widgets.tab_page import TabPage
from ui.widgets.page_header import FilterPanel
from ui.resources.icon_helper import get_icon
from ui.resources.table_helper import configure_table, refresh_table_theme, unhide_all_rows


class DevelopersTab(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.developer_controller = DeveloperController()
        self.export_controller = ExportController()
        self.init_ui()

    def init_ui(self):
        try:
            page = TabPage('Разработчики', 'Команда и ставки')
            outer = QVBoxLayout(self)
            outer.setContentsMargins(0, 0, 0, 0)
            outer.addWidget(page)
            main_layout = page.content_layout

            filter_panel = FilterPanel()
            fl = filter_panel.layout()

            search_label = QLabel("Поиск:")
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Имя разработчика")
            self.search_input.setMinimumWidth(220)
            self.search_input.textChanged.connect(self.apply_filters)

            position_label = QLabel("Должность:")
            self.position_combo = QComboBox()
            self.position_combo.setMinimumWidth(180)
            self.position_combo.addItem("Все", "")
            positions_result = self.developer_controller.get_developer_positions()
            if positions_result['success']:
                for position in positions_result['data']:
                    self.position_combo.addItem(position, position)
            self.position_combo.currentIndexChanged.connect(self.apply_filters)

            for w in [search_label, self.search_input, position_label, self.position_combo]:
                fl.addWidget(w)
            fl.addStretch()
            main_layout.addWidget(filter_panel)

            self.developers_table = QTableWidget()
            configure_table(self.developers_table)
            self.developers_table.setColumnCount(4)
            self.developers_table.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Ставка в час"])
            self.developers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.developers_table.setContextMenuPolicy(Qt.CustomContextMenu)
            self.developers_table.doubleClicked.connect(self.edit_item)

            main_layout.addWidget(self.developers_table)

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

            self.load_developers()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось инициализировать диалог: {str(e)}")

    def load_developers(self):
        self.developers_table.setRowCount(0)
        result = self.developer_controller.get_all_developers()

        if result['success']:
            for row, developer in enumerate(result['data']):
                self.developers_table.insertRow(row)

                id_item = QTableWidgetItem(str(developer.id))
                name_item = QTableWidgetItem(developer.full_name)
                position_item = QTableWidgetItem(developer.position)
                rate_item = QTableWidgetItem(str(developer.hourly_rate))

                self.developers_table.setItem(row, 0, id_item)
                self.developers_table.setItem(row, 1, name_item)
                self.developers_table.setItem(row, 2, position_item)
                self.developers_table.setItem(row, 3, rate_item)

            refresh_table_theme(self.developers_table)
            unhide_all_rows(self.developers_table)

    def apply_filters(self):
        search_text = self.search_input.text().lower()
        position = self.position_combo.currentData()

        for row in range(self.developers_table.rowCount()):
            name = self.developers_table.item(row, 1).text().lower()
            dev_position = self.developers_table.item(row, 2).text()
            should_show = search_text in name and (not position or dev_position == position)
            self.developers_table.setRowHidden(row, not should_show)

    def add_item(self):
        try:
            dialog = NewDeveloperDialog(self)
            if dialog.exec_():
                try:
                    developer_data = {
                        'full_name': dialog.name_input.text(),
                        'position': dialog.position_combo.currentText(),
                        'hourly_rate': float(dialog.rate_input.text())
                    }

                    result = self.developer_controller.create_developer(developer_data)
                    if result['success']:
                        QMessageBox.information(self, "Успех", "Разработчик успешно добавлен")
                        self.refresh_data()
                    else:
                        QMessageBox.critical(self, "Ошибка", result['error_message'])
                        return self.add_item()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при создании разработчика: {str(e)}")
                    return self.add_item()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при создании диалога: {str(e)}")

    def edit_item(self):
        try:
            selected_rows = self.developers_table.selectedItems()
            if not selected_rows:
                QMessageBox.warning(self, "Предупреждение", "Выберите разработчика для редактирования")
                return

            row = selected_rows[0].row()
            developer_id = int(self.developers_table.item(row, 0).text())
            result = self.developer_controller.get_developer_by_id(developer_id)

            if result['success']:
                dialog = NewDeveloperDialog(self, result['data'])
                if dialog.exec_():
                    try:
                        developer_data = {
                            'full_name': dialog.name_input.text(),
                            'position': dialog.position_combo.currentText(),
                            'hourly_rate': float(dialog.rate_input.text()),
                        }
                        update_result = self.developer_controller.update_developer(developer_id, developer_data)
                        if update_result['success']:
                            QMessageBox.information(self, "Успех", "Разработчик успешно обновлен")
                            self.refresh_data()
                        else:
                            QMessageBox.critical(self, "Ошибка", update_result['error_message'])
                            return self.edit_item()
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении разработчика: {str(e)}")
                        return self.edit_item()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при редактировании: {str(e)}")

    def delete_item(self):
        selected_rows = self.developers_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите разработчика для удаления")
            return

        row = selected_rows[0].row()
        developer_id = int(self.developers_table.item(row, 0).text())
        developer_name = self.developers_table.item(row, 1).text()

        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить разработчика '{developer_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            result = self.developer_controller.delete_developer(developer_id)
            if result['success']:
                QMessageBox.information(self, "Успех", "Разработчик успешно удален")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Ошибка", result['error_message'])

    def refresh_data(self):
        self.load_developers()
        self.apply_filters()

    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить CSV", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return

        headers = ["ID", "ФИО", "Должность", "Ставка в час"]
        data = []
        for row in range(self.developers_table.rowCount()):
            if not self.developers_table.isRowHidden(row):
                data.append([self.developers_table.item(row, col).text() for col in range(self.developers_table.columnCount())])

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

        headers = ["ID", "ФИО", "Должность", "Ставка в час"]
        data = []
        for row in range(self.developers_table.rowCount()):
            if not self.developers_table.isRowHidden(row):
                data.append([self.developers_table.item(row, col).text() for col in range(self.developers_table.columnCount())])

        result = self.export_controller.export_data_to_excel(data, headers, file_path, "Разработчики")
        if result['success']:
            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в {file_path}")
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
