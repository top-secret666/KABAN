from src.main.models import Task, Developer, Project
from utils import TaskValidator
from exceptions import BusinessException, ValidationException, DatabaseException


class TaskService:

    def get_all_tasks(self):
        try:
            query = """
                SELECT t.id, t.project_id, t.developer_id, t.description, t.status, 
                       t.hours_worked, t.created_at, t.updated_at,
                       p.name as project_name, d.full_name as developer_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN developers d ON t.developer_id = d.id
            """
            cursor = self.execute_query(query)

            tasks = []
            for row in cursor.fetchall():
                task = Task(
                    id=row[0],
                    project_id=row[1],
                    developer_id=row[2],
                    description=row[3],
                    status=row[4],
                    hours_worked=row[5],
                    created_at=row[6],
                    updated_at=row[7]
                )
                task.project_name = row[8]
                task.developer_name = row[9]
                tasks.append(task)

            return tasks
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка задач: {str(e)}")

    def get_task_by_id(self, task_id):
        try:
            task = Task.get_by_id(task_id)
            if task:
                project = task.get_project()
                developer = task.get_developer()
                task.project_name = project.name if project else None
                task.developer_name = developer.full_name if developer else None
            return task
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении задачи: {str(e)}")

    def create_task(self, data):
        try:
            validated_data = TaskValidator.validate(data)

            project = Project.get_by_id(validated_data['project_id'])
            if not project:
                raise BusinessException(f"Проект с ID {validated_data['project_id']} не найден")

            if validated_data.get('developer_id'):
                developer = Developer.get_by_id(validated_data['developer_id'])
                if not developer:
                    raise BusinessException(f"Разработчик с ID {validated_data['developer_id']} не найден")

            task = Task(
                project_id=validated_data['project_id'],
                developer_id=validated_data.get('developer_id'),
                description=validated_data['description'],
                status=validated_data.get('status', 'новая'),
                hours_worked=validated_data.get('hours_worked', 0)
            )

            success, error = task.save()
            if not success:
                raise BusinessException(f"Не удалось создать задачу: {error}")

            return task
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при создании задачи: {str(e)}")

    def update_task(self, task_id, data):
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                raise BusinessException(f"Задача с ID {task_id} не найдена")

            validated_data = TaskValidator.validate({
                'project_id': data.get('project_id', task.project_id),
                'developer_id': data.get('developer_id', task.developer_id),
                'description': data.get('description', task.description),
                'status': data.get('status', task.status),
                'hours_worked': data.get('hours_worked', task.hours_worked)
            })

            if 'project_id' in data and data['project_id'] != task.project_id:
                project = Project.get_by_id(validated_data['project_id'])
                if not project:
                    raise BusinessException(f"Проект с ID {validated_data['project_id']} не найден")

            if 'developer_id' in data and data['developer_id'] != task.developer_id:
                if validated_data.get('developer_id'):
                    developer = Developer.get_by_id(validated_data['developer_id'])
                    if not developer:
                        raise BusinessException(f"Разработчик с ID {validated_data['developer_id']} не найден")

            task.project_id = validated_data['project_id']
            task.developer_id = validated_data.get('developer_id')
            task.description = validated_data['description']
            task.status = validated_data['status']
            task.hours_worked = validated_data['hours_worked']

            success, error = task.save()
            if not success:
                raise BusinessException(f"Не удалось обновить задачу: {error}")

            return task
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении задачи: {str(e)}")

    def delete_task(self, task_id):
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                raise BusinessException(f"Задача с ID {task_id} не найдена")

            success, error = task.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить задачу: {error}")

            return True
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении задачи: {str(e)}")

    def assign_task(self, task_id, developer_id):
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                raise BusinessException(f"Задача с ID {task_id} не найдена")

            developer = Developer.get_by_id(developer_id)
            if not developer:
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")

            task.developer_id = developer_id

            if task.status == 'новая':
                task.status = 'в работе'

            success, error = task.save()
            if not success:
                raise BusinessException(f"Не удалось назначить задачу: {error}")

            return task
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при назначении задачи: {str(e)}")

    def update_task_status(self, task_id, status):
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                raise BusinessException(f"Задача с ID {task_id} не найдена")

            valid_statuses = ['новая', 'в работе', 'на проверке', 'завершено']
            if status not in valid_statuses:
                raise ValidationException(
                    f"Недопустимый статус. Допустимые значения: {', '.join(valid_statuses)}",
                    'status'
                )

            success, error = task.update_status(status)
            if not success:
                raise BusinessException(f"Не удалось обновить статус задачи: {error}")

            return task
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении статуса задачи: {str(e)}")

    def update_task_hours(self, task_id, hours):
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                raise BusinessException(f"Задача с ID {task_id} не найдена")

            try:
                hours = float(hours)
                if hours < 0:
                    raise ValueError("Часы должны быть положительным числом")
            except ValueError:
                raise ValidationException("Часы должны быть положительным числом", 'hours_worked')

            success, error = task.update_hours(hours)
            if not success:
                raise BusinessException(f"Не удалось обновить часы задачи: {error}")

            return task
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении часов задачи: {str(e)}")

    def search_tasks(self, search_term=None, project_id=None, developer_id=None, status=None):
        try:
            query = """
                SELECT t.id, t.project_id, t.developer_id, t.description, t.status, 
                       t.hours_worked, t.created_at, t.updated_at,
                       p.name as project_name, d.full_name as developer_name
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN developers d ON t.developer_id = d.id
                WHERE 1=1
            """
            params = []

            if search_term:
                query += " AND t.description LIKE ?"
                params.append(f"%{search_term}%")

            if project_id:
                query += " AND t.project_id = ?"
                params.append(project_id)

            if developer_id:
                query += " AND t.developer_id = ?"
                params.append(developer_id)

            if status:
                query += " AND t.status = ?"
                params.append(status)

            cursor = self.execute_query(query, params)

            tasks = []
            for row in cursor.fetchall():
                task = Task(
                    id=row[0],
                    project_id=row[1],
                    developer_id=row[2],
                    description=row[3],
                    status=row[4],
                    hours_worked=row[5],
                    created_at=row[6],
                    updated_at=row[7]
                )
                task.project_name = row[8]
                task.developer_name = row[9]
                tasks.append(task)

            return tasks
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при поиске задач: {str(e)}")
