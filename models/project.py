from .db_manager import DBManager
from datetime import datetime


class Project:
    def __init__(self, id=None, name=None, client=None, deadline=None, budget=None, status='в работе', created_by=None,
                 created_at=None, db_manager=None):
        self.id = id
        self.name = name
        self.client = client
        self.deadline = deadline
        self.budget = budget
        self.status = status
        self.db_manager = DBManager() if db_manager is None else db_manager
        self.created_at = created_at
        self.created_by = created_by

    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}', client='{self.client}', deadline='{self.deadline}', budget={self.budget}, status='{self.status}')"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'client': self.client,
            'deadline': self.deadline,
            'budget': self.budget,
            'status': self.status,
            'created_at': self.created_at,
            'created_by': self.created_by
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name', ""),
            client=data.get('client', ""),
            deadline=data.get('deadline', ""),
            budget=data.get('budget', 0),
            status=data.get('status', 'в работе'),
            created_at=data.get('created_at'),
            created_by=data.get('created_by')
        )

    def validate(self):
        if not self.name:
            return False, "Название проекта не может быть пустым"

        if not self.client:
            return False, "Клиент не может быть пустым"

        if not self.deadline:
            return False, "Срок сдачи не может быть пустым"

        try:
            datetime.strptime(self.deadline, '%Y-%m-%d')
        except ValueError:
            return False, "Срок сдачи должен быть в формате 'YYYY-MM-DD'"

        if self.budget < 0:
            return False, "Бюджет не может быть отрицательным"

        return True, None

    def save(self):
        is_valid, error_message = self.validate()
        if not is_valid:
            return False, error_message

        try:
            if self.id is None:
                self.db_manager.execute(
                    "INSERT INTO projects (name, client, deadline, budget, status, created_by) VALUES (?, ?, ?, ?, ?, ?)",
                    (self.name, self.client, self.deadline, self.budget, self.status, self.created_by)
                )
                self.id = self.db_manager.get_last_row_id()
            else:
                self.db_manager.execute(
                    "UPDATE projects SET name = ?, client = ?, deadline = ?, budget = ?, status = ? WHERE id = ?",
                    (self.name, self.client, self.deadline, self.budget, self.status, self.id)
                )

            self.db_manager.commit()
            return True, None

        except Exception as e:
            self.db_manager.rollback()
            return False, str(e)

    def delete(self):
        """
        Удаляет проект и все связанные с ним задачи
        """
        if self.id is None:
            return False, "Невозможно удалить несохраненный проект"

        try:
            # Начинаем транзакцию
            self.db_manager.begin_transaction()

            # Сначала удаляем все связанные задачи
            self.db_manager.execute(
                "DELETE FROM tasks WHERE project_id = ?",
                (self.id,)
            )

            # Затем удаляем сам проект
            self.db_manager.execute(
                "DELETE FROM projects WHERE id = ?",
                (self.id,)
            )

            # Фиксируем транзакцию
            self.db_manager.commit()

            self.id = None
            return True, None
        except Exception as e:
            # Откатываем транзакцию в случае ошибки
            self.db_manager.rollback()
            return False, str(e)

    @classmethod
    def get_by_id(cls, project_id):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM projects WHERE id = ?",
                (project_id,)
            )
            data = db_manager.fetch_one()

            if data:
                return cls.from_dict(data)
            return None

        except Exception as e:
            print(f"Ошибка при получении проекта: {e}")
            return None

    @classmethod
    def get_all(cls):
        db_manager = DBManager()
        try:
            db_manager.execute("SELECT * FROM projects")
            data_list = db_manager.fetch_all()

            # Отладочная информация
            print("Данные из базы данных:")
            for data in data_list:
                print(f"ID: {data.get('id')}, Название: {data.get('name')}, Статус: {data.get('status')}")

            return [cls.from_dict(data) for data in data_list]
        except Exception as e:
            print(f"Ошибка при получении проектов: {e}")
            return []

    @classmethod
    def get_by_client(cls, client):
        db_manager = DBManager()

        try:
            db_manager.execute(
                "SELECT * FROM projects WHERE client = ?",
                (client,)
            )
            data_list = db_manager.fetch_all()

            return [cls.from_dict(data) for data in data_list]

        except Exception as e:
            print(f"Ошибка при получении проектов: {e}")
            return []

    def get_tasks(self):
        if self.id is None:
            return []

        from .task import Task

        return Task.get_by_project(self.id)

    def get_progress(self):
        if self.id is None:
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'progress_percent': 0,
                'total_hours': 0,
                'days_left': 0,
                'labor_cost': 0
            }

        try:
            self.db_manager.execute(
                """
                SELECT 
                    COUNT(*) as total_tasks,
                    SUM(CASE WHEN status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                    SUM(hours_worked) as total_hours
                FROM tasks
                WHERE project_id = ?
                """,
                (self.id,)
            )
            result = self.db_manager.fetch_one()

            total_tasks = result['total_tasks']
            completed_tasks = result['completed_tasks'] or 0
            total_hours = result['total_hours'] or 0

            progress_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

            deadline_date = datetime.strptime(self.deadline, '%Y-%m-%d').date()
            today = datetime.now().date()
            days_left = (deadline_date - today).days

            self.db_manager.execute(
                """
                SELECT SUM(t.hours_worked * d.hourly_rate) as labor_cost
                FROM tasks t
                JOIN developers d ON t.developer_id = d.id
                WHERE t.project_id = ?
                """,
                (self.id,)
            )
            labor_result = self.db_manager.fetch_one()
            labor_cost = labor_result['labor_cost'] or 0

            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'progress_percent': progress_percent,
                'total_hours': total_hours,
                'days_left': days_left,
                'labor_cost': labor_cost
            }

        except Exception as e:
            print(f"Ошибка при получении прогресса проекта: {e}")
            return {
                'total_tasks': 0,
                'completed_tasks': 0,
                'progress_percent': 0,
                'total_hours': 0,
                'days_left': 0,
                'labor_cost': 0
            }

    def __str__(self):
        return f"Project(id={self.id}, name='{self.name}', client='{self.client}', deadline='{self.deadline}', budget={self.budget})"