from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QComboBox, QDateEdit, QGroupBox, QFormLayout, QTextBrowser,
                             QFileDialog, QMessageBox, QTabWidget, QDialog)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QDate

from src.main.service.controllers import ReportController, ExportController

class ReportsTab(QWidget):
    """
    Вкладка "Отчеты" - генерация и просмотр отчетов
    """
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.report_controller = ReportController()
        self.export_controller = ExportController()
        self.current_report_data = None
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
        
        title_label = QLabel("Отчеты")
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        header_layout.addWidget(title_label)
        
        main_layout.addLayout(header_layout)
        
        # Создание вкладок для разных типов отчетов
        self.tab_widget = QTabWidget()
        
        # Вкладка "Просроченные задачи"
        overdue_tab = QWidget()
        overdue_layout = QVBoxLayout(overdue_tab)
        
        # Кнопка генерации отчета
        overdue_button_layout = QHBoxLayout()
        
        generate_overdue_button = QPushButton("Сгенерировать отчет")
        generate_overdue_button.setIcon(QIcon('ui/resources/icons/report.png'))
        generate_overdue_button.clicked.connect(self.generate_overdue_tasks_report)
        
        export_overdue_button = QPushButton("Экспорт")
        export_overdue_button.setIcon(QIcon('ui/resources/icons/export.png'))
        export_overdue_button.clicked.connect(lambda: self.export_report("overdue"))
        
        overdue_button_layout.addWidget(generate_overdue_button)
        overdue_button_layout.addStretch()
        overdue_button_layout.addWidget(export_overdue_button)
        
        overdue_layout.addLayout(overdue_button_layout)
        
        # Область для отображения отчета
        self.overdue_report_browser = QTextBrowser()
        overdue_layout.addWidget(self.overdue_report_browser)
        
        # Вкладка "Загрузка разработчиков"
        workload_tab = QWidget()
        workload_layout = QVBoxLayout(workload_tab)
        
        # Параметры отчета
        workload_params_group = QGroupBox("Параметры отчета")
        workload_params_layout = QFormLayout()
        
        self.workload_date_from = QDateEdit()
        self.workload_date_from.setCalendarPopup(True)
        self.workload_date_from.setDate(QDate.currentDate().addMonths(-1))
        
        self.workload_date_to = QDateEdit()
        self.workload_date_to.setCalendarPopup(True)
        self.workload_date_to.setDate(QDate.currentDate())
        
        workload_params_layout.addRow("Дата начала:", self.workload_date_from)
        workload_params_layout.addRow("Дата окончания:", self.workload_date_to)
        
        workload_params_group.setLayout(workload_params_layout)
        workload_layout.addWidget(workload_params_group)
        
        # Кнопка генерации отчета
        workload_button_layout = QHBoxLayout()
        
        generate_workload_button = QPushButton("Сгенерировать отчет")
        generate_workload_button.setIcon(QIcon('ui/resources/icons/report.png'))
        generate_workload_button.clicked.connect(self.generate_developer_workload_report)
        
        export_workload_button = QPushButton("Экспорт")
        export_workload_button.setIcon(QIcon('ui/resources/icons/export.png'))
        export_workload_button.clicked.connect(lambda: self.export_report("workload"))
        
        workload_button_layout.addWidget(generate_workload_button)
        workload_button_layout.addStretch()
        workload_button_layout.addWidget(export_workload_button)
        
        workload_layout.addLayout(workload_button_layout)
        
        # Область для отображения отчета
        self.workload_report_browser = QTextBrowser()
        workload_layout.addWidget(self.workload_report_browser)
        
        # Вкладка "Статус проектов"
        project_status_tab = QWidget()
        project_status_layout = QVBoxLayout(project_status_tab)
        
        # Кнопка генерации отчета
        project_status_button_layout = QHBoxLayout()
        
        generate_project_status_button = QPushButton("Сгенерировать отчет")
        generate_project_status_button.setIcon(QIcon('ui/resources/icons/report.png'))
        generate_project_status_button.clicked.connect(self.generate_project_status_report)
        
        export_project_status_button = QPushButton("Экспорт")
        export_project_status_button.setIcon(QIcon('ui/resources/icons/export.png'))
        export_project_status_button.clicked.connect(lambda: self.export_report("project_status"))
        
        project_status_button_layout.addWidget(generate_project_status_button)
        project_status_button_layout.addStretch()
        project_status_button_layout.addWidget(export_project_status_button)
        
        project_status_layout.addLayout(project_status_button_layout)
        
        # Область для отображения отчета
        self.project_status_report_browser = QTextBrowser()
        project_status_layout.addWidget(self.project_status_report_browser)
        
        # Вкладка "Доходы за месяц"
        revenue_tab = QWidget()
        revenue_layout = QVBoxLayout(revenue_tab)
        
        # Параметры отчета
        revenue_params_group = QGroupBox("Параметры отчета")
        revenue_params_layout = QFormLayout()
        
        self.revenue_month_combo = QComboBox()
        for i in range(1, 13):
            self.revenue_month_combo.addItem(f"{i:02d}", i)
        
        # Установка текущего месяца
        current_month = QDate.currentDate().month()
        self.revenue_month_combo.setCurrentIndex(current_month - 1)
        
        self.revenue_year_combo = QComboBox()
        current_year = QDate.currentDate().year()
        for year in range(current_year - 5, current_year + 1):
            self.revenue_year_combo.addItem(str(year), year)
        
        # Установка текущего года
        self.revenue_year_combo.setCurrentIndex(5)  # Последний элемент (текущий год)
        
        revenue_params_layout.addRow("Месяц:", self.revenue_month_combo)
        revenue_params_layout.addRow("Год:", self.revenue_year_combo)
        
        revenue_params_group.setLayout(revenue_params_layout)
        revenue_layout.addWidget(revenue_params_group)
        
        # Кнопка генерации отчета
        revenue_button_layout = QHBoxLayout()
        
        generate_revenue_button = QPushButton("Сгенерировать отчет")
        generate_revenue_button.setIcon(QIcon('ui/resources/icons/report.png'))
        generate_revenue_button.clicked.connect(self.generate_monthly_revenue_report)
        
        export_revenue_button = QPushButton("Экспорт")
        export_revenue_button.setIcon(QIcon('ui/resources/icons/export.png'))
        export_revenue_button.clicked.connect(lambda: self.export_report("revenue"))
        
        revenue_button_layout.addWidget(generate_revenue_button)
        revenue_button_layout.addStretch()
        revenue_button_layout.addWidget(export_revenue_button)
        
        revenue_layout.addLayout(revenue_button_layout)
        
        # Область для отображения отчета
        self.revenue_report_browser = QTextBrowser()
        revenue_layout.addWidget(self.revenue_report_browser)
        
        # Добавление вкладок
        self.tab_widget.addTab(overdue_tab, "Просроченные задачи")
        self.tab_widget.addTab(workload_tab, "Загрузка разработчиков")
        self.tab_widget.addTab(project_status_tab, "Статус проектов")
        self.tab_widget.addTab(revenue_tab, "Доходы за месяц")
        
        main_layout.addWidget(self.tab_widget)
    
    def generate_overdue_tasks_report(self):
        """
        Генерация отчета по просроченным задачам
        """
        # Получение отчета
        result = self.report_controller.get_overdue_tasks_report()
        
        if result['success']:
            report_data = result['data']
            self.current_report_data = report_data
            
            # Формирование HTML для отображения
            html = f"""
            <h2>{report_data['report_name']}</h2>
            <p>Дата генерации: {report_data['generated_at']}</p>
            <p>Всего просроченных задач: {report_data['total_tasks']}</p>
            
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
                <tr bgcolor="#f0f0f0">
                    <th>ID</th>
                    <th>Описание</th>
                    <th>Статус</th>
                    <th>Часы</th>
                    <th>Проект</th>
                    <th>Дедлайн</th>
                    <th>Разработчик</th>
                </tr>
            """
            
            for task in report_data['tasks']:
                html += f"""
                <tr>
                    <td>{task['id']}</td>
                    <td>{task['description']}</td>
                    <td>{task['status']}</td>
                    <td>{task['hours_worked']}</td>
                    <td>{task['project_name']}</td>
                    <td>{task['project_deadline']}</td>
                    <td>{task['developer_name'] or 'Не назначен'}</td>
                </tr>
                """
            
            html += "</table>"
            
            # Отображение отчета
            self.overdue_report_browser.setHtml(html)
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def generate_developer_workload_report(self):
        """
        Генерация отчета по загрузке разработчиков
        """
        # Получение параметров
        start_date = self.workload_date_from.date().toString("yyyy-MM-dd")
        end_date = self.workload_date_to.date().toString("yyyy-MM-dd")
        
        # Получение отчета
        result = self.report_controller.get_developer_workload_report(start_date, end_date)
        
        if result['success']:
            report_data = result['data']
            self.current_report_data = report_data
            
            # Формирование HTML для отображения
            html = f"""
            <h2>{report_data['report_name']}</h2>
            <p>Дата генерации: {report_data['generated_at']}</p>
            <p>Период: {report_data['start_date']} - {report_data['end_date']}</p>
            <p>Всего разработчиков: {report_data['total_developers']}</p>
            <p>Общее количество часов: {report_data['total_hours']}</p>
            <p>Общая стоимость: {report_data['total_cost']} руб.</p>
            
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
                <tr bgcolor="#f0f0f0">
                    <th>ID</th>
                    <th>ФИО</th>
                    <th>Должность</th>
                    <th>Ставка</th>
                    <th>Кол-во задач</th>
                    <th>Часы</th>
                    <th>Стоимость</th>
                </tr>
            """
            
            for dev in report_data['developers']:
                html += f"""
                <tr>
                    <td>{dev['id']}</td>
                    <td>{dev['full_name']}</td>
                    <td>{dev['position']}</td>
                    <td>{dev['hourly_rate']}</td>
                    <td>{dev['task_count']}</td>
                    <td>{dev['total_hours']}</td>
                    <td>{dev['total_cost']}</td>
                </tr>
                """
            
            html += "</table>"
            
            # Отображение отчета
            self.workload_report_browser.setHtml(html)
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def generate_project_status_report(self):
        """
        Генерация отчета по статусу проектов
        """
        # Получение отчета
        result = self.report_controller.get_project_status_report()
        
        if result['success']:
            report_data = result['data']
            self.current_report_data = report_data
            
            # Формирование HTML для отображения
            html = f"""
            <h2>{report_data['report_name']}</h2>
            <p>Дата генерации: {report_data['generated_at']}</p>
            <p>Всего проектов: {report_data['total_projects']}</p>
            <p>Просроченных проектов: {report_data['overdue_projects']}</p>
            <p>Завершенных проектов: {report_data['completed_projects']}</p>
            <p>Общий бюджет: {report_data['total_budget']} руб.</p>
            <p>Общая стоимость: {report_data['total_cost']} руб.</p>
            
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
                <tr bgcolor="#f0f0f0">
                    <th>ID</th>
                    <th>Название</th>
                    <th>Клиент</th>
                    <th>Дедлайн</th>
                    <th>Бюджет</th>
                    <th>Задачи</th>
                    <th>Завершено</th>
                    <th>Прогресс</th>
                    <th>Часы</th>
                    <th>Стоимость</th>
                </tr>
            """
            
            for proj in report_data['projects']:
                # Определение цвета строки в зависимости от статуса
                row_color = ""
                if proj['is_overdue']:
                    row_color = ' bgcolor="#FFCDD2"'  # Красный для просроченных
                elif proj['progress_percent'] == 100:
                    row_color = ' bgcolor="#C8E6C9"'  # Зеленый для завершенных
                
                html += f"""
                <tr{row_color}>
                    <td>{proj['id']}</td>
                    <td>{proj['name']}</td>
                    <td>{proj['client']}</td>
                    <td>{proj['deadline']}</td>
                    <td>{proj['budget']}</td>
                    <td>{proj['total_tasks']}</td>
                    <td>{proj['completed_tasks']}</td>
                    <td>{proj['progress_percent']}%</td>
                    <td>{proj['total_hours']}</td>
                    <td>{proj['total_cost']}</td>
                </tr>
                """
            
            html += "</table>"
            
            # Отображение отчета
            self.project_status_report_browser.setHtml(html)
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def generate_monthly_revenue_report(self):
        """
        Генерация отчета по доходам за месяц
        """
        # Получение параметров
        year = self.revenue_year_combo.currentData()
        month = self.revenue_month_combo.currentData()
        
        # Получение отчета
        result = self.report_controller.get_monthly_revenue_report(year, month)
        
        if result['success']:
            report_data = result['data']
            self.current_report_data = report_data
            
            # Формирование HTML для отображения
            html = f"""
            <h2>{report_data['report_name']}</h2>
            <p>Дата генерации: {report_data['generated_at']}</p>
            <p>Период: {report_data['start_date']} - {report_data['end_date']}</p>
            <p>Всего проектов: {report_data['total_projects']}</p>
            <p>Общий бюджет: {report_data['total_budget']} руб.</p>
            <p>Общая стоимость: {report_data['total_cost']} руб.</p>
            <p>Общая прибыль: {report_data['total_profit']} руб.</p>
            
            <table border="1" cellspacing="0" cellpadding="5" width="100%">
                <tr bgcolor="#f0f0f0">
                    <th>ID</th>
                    <th>Название</th>
                    <th>Клиент</th>
                    <th>Бюджет</th>
                    <th>Задачи</th>
                    <th>Часы</th>
                    <th>Стоимость</th>
                    <th>Прибыль</th>
                </tr>
            """
            
            for proj in report_data['projects']:
                # Определение цвета строки в зависимости от прибыли
                row_color = ""
                if proj['profit'] and proj['profit'] < 0:
                    row_color = ' bgcolor="#FFCDD2"'  # Красный для убыточных
                elif proj['profit'] and proj['profit'] > 0:
                    row_color = ' bgcolor="#C8E6C9"'  # Зеленый для прибыльных
                
                html += f"""
                <tr{row_color}>
                    <td>{proj['id']}</td>
                    <td>{proj['name']}</td>
                    <td>{proj['client']}</td>
                    <td>{proj['budget']}</td>
                    <td>{proj['task_count']}</td>
                    <td>{proj['total_hours']}</td>
                    <td>{proj['total_cost']}</td>
                    <td>{proj['profit'] if proj['profit'] is not None else 'Н/Д'}</td>
                </tr>
                """
            
            html += "</table>"
            
            # Отображение отчета
            self.revenue_report_browser.setHtml(html)
        else:
            QMessageBox.critical(self, "Ошибка", result['error_message'])
    
    def export_report(self, report_type):
        """
        Экспорт отчета в CSV или Excel
        """
        if not self.current_report_data:
            QMessageBox.warning(self, "Предупреждение", "Сначала сгенерируйте отчет")
            return
        
        # Открытие диалога выбора формата
        format_dialog = QDialog(self)
        format_dialog.setWindowTitle("Выбор формата")
        format_dialog.setMinimumWidth(300)
        
        format_layout = QVBoxLayout(format_dialog)
        
        format_label = QLabel("Выберите формат экспорта:")
        format_layout.addWidget(format_label)
        
        format_combo = QComboBox()
        format_combo.addItem("CSV", "csv")
        format_combo.addItem("Excel", "excel")
        format_layout.addWidget(format_combo)
        
        buttons_layout = QHBoxLayout()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(format_dialog.accept)
        
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(format_dialog.reject)
        
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        
        format_layout.addLayout(buttons_layout)
        
        # Если пользователь выбрал формат
        if format_dialog.exec_():
            export_format = format_combo.currentData()
            
            # Открытие диалога сохранения файла
            if export_format == "csv":
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить CSV", "", "CSV Files (*.csv);;All Files (*)"
                )
                
                if file_path:
                    # Экспорт в CSV
                    result = self.export_controller.export_report_to_csv(self.current_report_data, file_path)
                    
                    if result['success']:
                        QMessageBox.information(self, "Успех", f"Отчет успешно экспортирован в {file_path}")
                    else:
                        QMessageBox.critical(self, "Ошибка", result['error_message'])
            
            elif export_format == "excel":
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "Сохранить Excel", "", "Excel Files (*.xlsx);;All Files (*)"
                )
                
                if file_path:
                    # Экспорт в Excel
                    result = self.export_controller.export_report_to_excel(self.current_report_data, file_path)
                    
                    if result['success']:
                        QMessageBox.information(self, "Успех", f"Отчет успешно экспортирован в {file_path}")
                    else:
                        QMessageBox.critical(self, "Ошибка", result['error_message'])
