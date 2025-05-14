from src.main.models import Project, Task
from utils import ProjectValidator
from exceptions import BusinessException, ValidationException, DatabaseException
from datetime import datetime


class ProjectService:

    def get_all_projects(self):

        try:
            query = "SELECT id, name, client, deadline, budget, created_at FROM projects"
            cursor = self.execute_query(query)

            projects = []
            for row in cursor.fetchall():
                project = Project(
                    id=row[0],
                    name=row[1],
                    client=row[2],
                    deadline=row[3],
                    budget=row[4],
                    created_at=row[5]
                )
                projects.append(project)

            return projects
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка проектов: {str(e)}")

    def get_project_by_id(self, project_id):

        try:
            return Project.get_by_id(project_id)
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении проекта: {str(e)}")

    def create_project(self, data):

        try:
            validated_data = ProjectValidator.validate(data)

            project = Project(
                name=validated_data['name'],
                client=validated_data['client'],
                deadline=validated_data.get('deadline'),
                budget=validated_data.get('budget', 0)
            )

            success, error = project.save()
            if not success:
                raise BusinessException(f"Не удалось создать проект: {error}")

            return project
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при создании проекта: {str(e)}")

    def update_project(self, project_id, data):

        try:
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")

            validated_data = ProjectValidator.validate(data)

            project.name = validated_data['name']
            project.client = validated_data['client']
            project.deadline = validated_data.get('deadline', project.deadline)
            project.budget = validated_data.get('budget', project.budget)

            success, error = project.save()
            if not success:
                raise BusinessException(f"Не удалось обновить проект: {error}")

            return project
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении проекта: {str(e)}")

    def delete_project(self, project_id):
        try:
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")

            tasks = project.get_tasks()
            if tasks:
                for task in tasks:
                    task.delete()

            success, error = project.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить проект: {error}")

            return True
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении проекта: {str(e)}")

    def search_projects(self, search_term=None, client=None, start_date=None, end_date=None):
        try:
            query = "SELECT id, name, client, deadline, budget, created_at FROM projects WHERE 1=1"
            params = []

            if search_term:
                query += " AND (name LIKE ? OR client LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])

            if client:
                query += " AND client LIKE ?"
                params.append(f"%{client}%")

            if start_date:
                query += " AND date(deadline) >= date(?)"
                params.append(start_date)

            if end_date:
                query += " AND date(deadline) <= date(?)"
                params.append(end_date)

            cursor = self.execute_query(query, params)

            projects = []
            for row in cursor.fetchall():
                project = Project(
                    id=row[0],
                    name=row[1],
                    client=row[2],
                    deadline=row[3],
                    budget=row[4],
                    created_at=row[5]
                )
                projects.append(project)

            return projects
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при поиске проектов: {str(e)}")

    def get_project_progress(self, project_id):
        try:
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")

            return project.get_progress()
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении прогресса проекта: {str(e)}")

    def get_project_cost(self, project_id):
        try:
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")

            tasks = project.get_tasks()

            total_cost = 0
            for task in tasks:
                developer = task.get_developer()
                if developer:
                    total_cost += task.hours_worked * developer.hourly_rate

            return {
                'project': project,
                'total_hours': sum(task.hours_worked for task in tasks),
                'total_cost': total_cost,
                'budget': project.budget,
                'budget_remaining': project.budget - total_cost if project.budget else None
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при расчете стоимости проекта: {str(e)}")

    def get_overdue_projects(self):
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            query = """
                SELECT id, name, client, deadline, budget, created_at 
                FROM projects 
                WHERE deadline < ? AND deadline IS NOT NULL
            """
            cursor = self.execute_query(query, [today])

            projects = []
            for row in cursor.fetchall():
                project = Project(
                    id=row[0],
                    name=row[1],
                    client=row[2],
                    deadline=row[3],
                    budget=row[4],
                    created_at=row[5]
                )
                projects.append(project)

            return projects
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении просроченных проектов: {str(e)}")
