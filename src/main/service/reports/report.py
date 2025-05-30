from src.main.service.exceptions import BusinessException, ValidationException, DatabaseException
from datetime import datetime, timedelta


class ReportService:
    def get_overdue_tasks_report(self):
        try:
            query = """
                SELECT t.id, t.description, t.status, t.hours_worked, 
                       p.id as project_id, p.name as project_name, p.deadline as project_deadline,
                       d.id as developer_id, d.full_name as developer_name
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                LEFT JOIN developers d ON t.developer_id = d.id
                WHERE p.deadline < date('now') AND p.deadline IS NOT NULL
                AND t.status != 'завершено'
                ORDER BY p.deadline ASC
            """
            cursor = self.execute_query(query)

            tasks = []
            for row in cursor.fetchall():
                task = {
                    'id': row[0],
                    'description': row[1],
                    'status': row[2],
                    'hours_worked': row[3],
                    'project_id': row[4],
                    'project_name': row[5],
                    'project_deadline': row[6],
                    'developer_id': row[7],
                    'developer_name': row[8]
                }
                tasks.append(task)

            return {
                'report_name': 'Отчет по просроченным задачам',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tasks': tasks,
                'total_tasks': len(tasks)
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при генерации отчета по просроченным задачам: {str(e)}")

    def get_developer_workload_report(self, start_date=None, end_date=None):
        try:
            if not start_date:
                today = datetime.now()
                start_date = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')

            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')

            query = """
                SELECT d.id, d.full_name, d.position, d.hourly_rate,
                       COUNT(t.id) as task_count,
                       SUM(t.hours_worked) as total_hours,
                       SUM(t.hours_worked * d.hourly_rate) as total_cost
                FROM developers d
                LEFT JOIN tasks t ON d.id = t.developer_id
                WHERE (t.created_at IS NULL OR (date(t.created_at) >= date(?) AND date(t.created_at) <= date(?)))
                GROUP BY d.id
                ORDER BY total_hours DESC
            """
            cursor = self.execute_query(query, [start_date, end_date])

            developers = []
            for row in cursor.fetchall():
                developer = {
                    'id': row[0],
                    'full_name': row[1],
                    'position': row[2],
                    'hourly_rate': row[3],
                    'task_count': row[4] or 0,
                    'total_hours': row[5] or 0,
                    'total_cost': row[6] or 0
                }
                developers.append(developer)

            return {
                'report_name': 'Отчет по загрузке разработчиков',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'start_date': start_date,
                'end_date': end_date,
                'developers': developers,
                'total_developers': len(developers),
                'total_hours': sum(dev['total_hours'] for dev in developers),
                'total_cost': sum(dev['total_cost'] for dev in developers)
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при генерации отчета по загрузке разработчиков: {str(e)}")

    def get_project_status_report(self):
        try:
            query = """
                SELECT p.id, p.name, p.client, p.deadline, p.budget,
                       COUNT(t.id) as total_tasks,
                       SUM(CASE WHEN t.status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                       SUM(t.hours_worked) as total_hours,
                       SUM(t.hours_worked * d.hourly_rate) as total_cost
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                LEFT JOIN developers d ON t.developer_id = d.id
                GROUP BY p.id
                ORDER BY p.deadline ASC
            """
            cursor = self.execute_query(query)

            projects = []
            for row in cursor.fetchall():
                total_tasks = row[5] or 0
                completed_tasks = row[6] or 0
                progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

                project = {
                    'id': row[0],
                    'name': row[1],
                    'client': row[2],
                    'deadline': row[3],
                    'budget': row[4],
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'progress_percent': round(progress_percent, 2),
                    'total_hours': row[7] or 0,
                    'total_cost': row[8] or 0,
                    'budget_remaining': (row[4] - (row[8] or 0)) if row[4] else None,
                    'is_overdue': row[3] and datetime.strptime(row[3], '%Y-%m-%d').date() < datetime.now().date(),
                    'days_remaining': (datetime.strptime(row[3], '%Y-%m-%d').date() - datetime.now().date()).days if
                    row[3] else None
                }
                projects.append(project)

            return {
                'report_name': 'Отчет по статусу проектов',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'projects': projects,
                'total_projects': len(projects),
                'overdue_projects': sum(1 for p in projects if p['is_overdue']),
                'completed_projects': sum(1 for p in projects if p['progress_percent'] == 100),
                'total_budget': sum(p['budget'] for p in projects if p['budget']),
                'total_cost': sum(p['total_cost'] for p in projects)
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при генерации отчета по статусу проектов: {str(e)}")

    def get_monthly_revenue_report(self, year=None, month=None):
        try:
            if not year or not month:
                today = datetime.now()
                year = year or today.year
                month = month or today.month

            start_date = datetime(year, month, 1).strftime('%Y-%m-%d')

            if month == 12:
                end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = datetime(year, month + 1, 1) - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')

            query = """
                SELECT p.id, p.name, p.client, p.budget,
                       COUNT(t.id) as task_count,
                       SUM(t.hours_worked) as total_hours,
                       SUM(t.hours_worked * d.hourly_rate) as total_cost
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                LEFT JOIN developers d ON t.developer_id = d.id
                WHERE date(t.created_at) >= date(?) AND date(t.created_at) <= date(?)
                GROUP BY p.id
                ORDER BY total_cost DESC
            """
            cursor = self.execute_query(query, [start_date, end_date])

            projects = []
            for row in cursor.fetchall():
                project = {
                    'id': row[0],
                    'name': row[1],
                    'client': row[2],
                    'budget': row[3],
                    'task_count': row[4] or 0,
                    'total_hours': row[5] or 0,
                    'total_cost': row[6] or 0,
                    'profit': (row[3] - (row[6] or 0)) if row[3] else None
                }
                projects.append(project)

            return {
                'report_name': f'Отчет по доходам за {month}/{year}',
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'year': year,
                'month': month,
                'start_date': start_date,
                'end_date': end_date,
                'projects': projects,
                'total_projects': len(projects),
                'total_budget': sum(p['budget'] for p in projects if p['budget']),
                'total_cost': sum(p['total_cost'] for p in projects),
                'total_profit': sum(p['profit'] for p in projects if p['profit'] is not None)
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при генерации отчета по доходам за месяц: {str(e)}")
