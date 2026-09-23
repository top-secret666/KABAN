from services.base_service import BaseService
from models import Project, Task
from validation import ProjectValidator
from exceptions import BusinessException, ValidationException, DatabaseException
from datetime import datetime

class ProjectService(BaseService):
    """
    Сервис для работы с проектами
    """

    def get_all_projects(self):
        """
        Получает список всех проектов
        """
        try:
            query = "SELECT id, name, client, deadline, budget, status, created_at FROM projects"
            cursor = self.execute_query(query)

            projects = []
            for row in cursor.fetchall():
                project = Project(
                    id=row[0],
                    name=row[1],
                    client=row[2],
                    deadline=row[3],
                    budget=row[4],
                    status=row[5],
                    created_at=row[6]
                )
                projects.append(project)

            return projects
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка проектов: {str(e)}")

    def get_project_by_id(self, project_id):
        """
        Получает проект по ID
        """
        query = "SELECT * FROM projects WHERE id = ?"
        result = self.db_manager.execute(query, (project_id,)).fetchone()

        if not result:
            raise BusinessException(f"Проект с ID {project_id} не найден")

        return Project(*result)

    def create_project(self, data):
        """
        Создает новый проект или обновляет существующий, если найден дубликат
        """
        try:
            # Валидация данных
            validated_data = ProjectValidator.validate(data)
            
            # Проверка на дубликаты по названию и клиенту
            query = "SELECT id FROM projects WHERE name = ? AND client = ?"
            cursor = self.execute_query(query, [validated_data['name'], validated_data['client']])
            existing_project = cursor.fetchone()
            
            if existing_project:
                # Если проект с таким названием и клиентом уже существует, обновляем его
                project_id = existing_project[0]
                project = Project.get_by_id(project_id)
                
                # Обновляем только те поля, которые предоставлены
                if 'deadline' in validated_data:
                    project.deadline = validated_data['deadline']
                if 'budget' in validated_data:
                    project.budget = validated_data['budget']
                
                # Сохраняем изменения
                success, error = project.save()
                if not success:
                    raise BusinessException(f"Не удалось обновить существующий проект: {error}")
                
                return project
            else:
                # Создание нового объекта проекта
                project = Project(
                    name=validated_data['name'],
                    client=validated_data['client'],
                    deadline=validated_data.get('deadline'),
                    budget=validated_data.get('budget', 0)
                )
                
                # Сохранение в базу данных
                success, error = project.save()
                if not success:
                    raise BusinessException(f"Не удалось создать проект: {error}")
                
                return project
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при создании/обновлении проекта: {str(e)}")
    
    def update_project(self, project_id, data):
        """
        Обновляет данные проекта
        """
        try:
            # Получение проекта
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")
            
            # Валидация данных
            validated_data = ProjectValidator.validate(data)
            
            # Обновление полей
            project.name = validated_data['name']
            project.client = validated_data['client']
            project.deadline = validated_data.get('deadline', project.deadline)
            project.budget = validated_data.get('budget', project.budget)
            
            # Сохранение изменений
            success, error = project.save()
            if not success:
                raise BusinessException(f"Не удалось обновить проект: {error}")
            
            return project
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении проекта: {str(e)}")

    def delete_project(self, project_id):
        """
        Удаляет проект и все связанные с ним задачи
        """
        try:
            # Получение проекта
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")

            # Начинаем транзакцию
            self.db_manager.begin_transaction()

            # Сначала удаляем все связанные задачи
            self.db_manager.execute(
                "DELETE FROM tasks WHERE project_id = ?",
                (project_id,)
            )

            # Затем удаляем сам проект
            self.db_manager.execute(
                "DELETE FROM projects WHERE id = ?",
                (project_id,)
            )

            # Фиксируем транзакцию
            self.db_manager.commit()

            return True
        except Exception as e:
            # Откатываем транзакцию в случае ошибки
            self.db_manager.rollback()

            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении проекта: {str(e)}")

    def search_projects(self, search_term=None, client=None, start_date=None, end_date=None):
        """
        Поиск проектов по названию, клиенту и/или дате
        """
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
        """
        Получает прогресс проекта
        """
        try:
            # Получение проекта
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")
            
            return project.get_progress()
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении прогресса проекта: {str(e)}")
    
    def get_project_cost(self, project_id):
        """
        Расчет стоимости проекта на основе затраченных часов
        """
        try:
            # Получение проекта
            project = self.get_project_by_id(project_id)
            if not project:
                raise BusinessException(f"Проект с ID {project_id} не найден")
            
            # Получение задач проекта
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
        """
        Получает список просроченных проектов
        """
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
