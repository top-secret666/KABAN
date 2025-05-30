from src.main.service.reports import ReportService


class ReportController:
    def __init__(self, service=None):
        super().__init__(service or ReportService())

    def get_overdue_tasks_report(self):
        return self.execute_service_method('get_overdue_tasks_report')

    def get_developer_workload_report(self, start_date=None, end_date=None):
        return self.execute_service_method('get_developer_workload_report', start_date, end_date)

    def get_project_status_report(self):
        return self.execute_service_method('get_project_status_report')

    def get_monthly_revenue_report(self, year=None, month=None):
        return self.execute_service_method('get_monthly_revenue_report', year, month)

    def export_report_to_csv(self, report_data, filename):
        try:
            import csv
            import os

            report_type = report_data.get('report_name', '').lower()

            if 'просроченным задачам' in report_type:
                headers = ['ID', 'Описание', 'Статус', 'Часы', 'Проект', 'Дедлайн', 'Разработчик']
                rows = []
                for task in report_data.get('tasks', []):
                    rows.append([
                        task.get('id', ''),
                        task.get('description', ''),
                        task.get('status', ''),
                        task.get('hours_worked', ''),
                        task.get('project_name', ''),
                        task.get('project_deadline', ''),
                        task.get('developer_name', '')
                    ])

            elif 'загрузке разработчиков' in report_type:
                headers = ['ID', 'ФИО', 'Должность', 'Ставка', 'Кол-во задач', 'Часы', 'Стоимость']
                rows = []
                for dev in report_data.get('developers', []):
                    rows.append([
                        dev.get('id', ''),
                        dev.get('full_name', ''),
                        dev.get('position', ''),
                        dev.get('hourly_rate', ''),
                        dev.get('task_count', ''),
                        dev.get('total_hours', ''),
                        dev.get('total_cost', '')
                    ])

            elif 'статусу проектов' in report_type:
                headers = ['ID', 'Название', 'Клиент', 'Дедлайн', 'Бюджет', 'Задачи', 'Завершено', 'Прогресс', 'Часы',
                           'Стоимость']
                rows = []
                for proj in report_data.get('projects', []):
                    rows.append([
                        proj.get('id', ''),
                        proj.get('name', ''),
                        proj.get('client', ''),
                        proj.get('deadline', ''),
                        proj.get('budget', ''),
                        proj.get('total_tasks', ''),
                        proj.get('completed_tasks', ''),
                        f"{proj.get('progress_percent', '')}%",
                        proj.get('total_hours', ''),
                        proj.get('total_cost', '')
                    ])

            elif 'доходам за месяц' in report_type:
                headers = ['ID', 'Название', 'Клиент', 'Бюджет', 'Задачи', 'Часы', 'Стоимость', 'Прибыль']
                rows = []
                for proj in report_data.get('projects', []):
                    rows.append([
                        proj.get('id', ''),
                        proj.get('name', ''),
                        proj.get('client', ''),
                        proj.get('budget', ''),
                        proj.get('task_count', ''),
                        proj.get('total_hours', ''),
                        proj.get('total_cost', ''),
                        proj.get('profit', '')
                    ])

            else:
                # Общий случай
                if isinstance(report_data.get('data', []), list) and len(report_data.get('data', [])) > 0:
                    first_item = report_data['data'][0]
                    headers = list(first_item.keys())
                    rows = [list(item.values()) for item in report_data['data']]
                else:
                    return {
                        'success': False,
                        'error_type': 'Ошибка экспорта',
                        'error_message': 'Неизвестный формат отчета'
                    }

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)

            return {
                'success': True,
                'data': {
                    'filename': filename,
                    'rows_count': len(rows)
                }
            }

        except Exception as e:
            return self.handle_exception(e)
