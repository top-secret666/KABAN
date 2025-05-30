from controllers.base_controller import BaseController
from models import Project
from services import ProjectService

class ProjectController(BaseController):
    """
    Контроллер для управления проектами
    """
    def __init__(self, service=None):
        """
        Инициализирует контроллер с сервисом проектов
        """
        super().__init__(service or ProjectService())
    
    def get_all_projects(self):
        """
        Получает список всех проектов
        """
        return self.execute_service_method('get_all_projects')

    def get_project_by_id(self, project_id):
        """
        Получает проект по ID
        """
        return self.execute_service_method('get_project_by_id', project_id)

    def get_projects_by_developer(self, developer_id):
        """
        Получение списка проектов, в которых участвует указанный разработчик

        Args:
            developer_id (int): ID разработчика

        Returns:
            dict: Результат операции с ключами:
                - success (bool): Успешность операции
                - data (list): Список объектов проектов или None в случае ошибки
                - error_message (str): Сообщение об ошибке или None в случае успеха
        """
        try:
            from models import DBManager

            print(f"Получение проектов для разработчика с ID: {developer_id}")

            # Создаем экземпляр DBManager
            db_manager = DBManager()
            db_manager.connect()

            # Проверяем существование разработчика
            check_query = "SELECT id, full_name FROM developers WHERE id = ?"
            db_manager.execute(check_query, (developer_id,))
            developer = db_manager.fetch_one()

            if not developer:
                print(f"Разработчик с ID {developer_id} не найден в базе данных")
                return {
                    'success': False,
                    'data': None,
                    'error_message': f"Разработчик с ID {developer_id} не найден"
                }

            print(f"Найден разработчик: {developer['full_name']} (ID: {developer['id']})")

            # Получаем задачи разработчика
            tasks_query = """
                SELECT DISTINCT project_id FROM tasks 
                WHERE developer_id = ?
            """
            db_manager.execute(tasks_query, (developer_id,))
            tasks_result = db_manager.fetch_all()

            print(f"Найдено задач с уникальными project_id: {len(tasks_result) if tasks_result else 0}")

            if not tasks_result:
                print("У разработчика нет задач, связанных с проектами")
                return {
                    'success': True,
                    'data': [],
                    'error_message': None
                }

            # Получаем ID проектов, в которых участвует разработчик
            project_ids = [row['project_id'] for row in tasks_result]
            print(f"ID проектов: {project_ids}")

            if not project_ids:
                # Если у разработчика нет задач, возвращаем пустой список
                print("Список ID проектов пуст")
                return {
                    'success': True,
                    'data': [],
                    'error_message': None
                }

            # Формируем строку с параметрами для SQL запроса
            placeholders = ', '.join(['?'] * len(project_ids))

            # Получаем проекты по их ID - исправлено: убрана колонка description, которой нет в таблице
            projects_query = f"""
                SELECT id, name, client, deadline, budget, status, created_at 
                FROM projects 
                WHERE id IN ({placeholders})
            """
            db_manager.execute(projects_query, project_ids)
            projects_result = db_manager.fetch_all()

            print(f"Найдено проектов: {len(projects_result) if projects_result else 0}")

            if not projects_result:
                print("Проекты не найдены")
                return {
                    'success': True,
                    'data': [],
                    'error_message': None
                }

            # Преобразуем результаты в объекты Project
            from models.project import Project
            projects = []
            for row in projects_result:
                print(f"Обработка проекта: ID={row['id']}, Название={row['name']}")
                # Создаем объект Project только с теми параметрами, которые он принимает
                project = Project(
                    id=row['id'],
                    name=row['name'],
                    client=row['client'],
                    deadline=row['deadline'],
                    budget=row['budget'],
                    status=row['status'],
                    created_at=row.get('created_at', '')
                    # Убрали параметры description и updated_at
                )
                projects.append(project)

            return {
                'success': True,
                'data': projects,
                'error_message': None
            }
        except Exception as e:
            import traceback
            print(f"Ошибка при получении проектов разработчика: {str(e)}")
            print(traceback.format_exc())
            return {
                'success': False,
                'data': None,
                'error_message': f"Ошибка при получении проектов разработчика: {str(e)}"
            }

    def create_project(self, data):
        """
        Создает новый проект
        """
        return self.execute_service_method('create_project', data)
    
    def update_project(self, project_id, data):
        """
        Обновляет данные проекта
        """
        return self.execute_service_method('update_project', project_id, data)
    
    def delete_project(self, project_id):
        """
        Удаляет проект
        """
        return self.execute_service_method('delete_project', project_id)
    
    def search_projects(self, search_term=None, client=None, start_date=None, end_date=None):
        """
        Поиск проектов по названию, клиенту и/или дате
        """
        return self.execute_service_method('search_projects', search_term, client, start_date, end_date)
    
    def get_project_progress(self, project_id):
        """
        Получает прогресс проекта
        """
        return self.execute_service_method('get_project_progress', project_id)
    
    def get_project_cost(self, project_id):
        """
        Расчет стоимости проекта на основе затраченных часов
        """
        return self.execute_service_method('get_project_cost', project_id)
    
    def get_overdue_projects(self):
        """
        Получает список просроченных проектов
        """
        return self.execute_service_method('get_overdue_projects')
