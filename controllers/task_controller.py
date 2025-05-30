from controllers.base_controller import BaseController
from services import TaskService

class TaskController(BaseController):
    """
    Контроллер для управления задачами
    """
    def __init__(self, service=None):
        """
        Инициализирует контроллер с сервисом задач
        """
        super().__init__(service or TaskService())
    
    def get_all_tasks(self):
        """
        Получает список всех задач
        """
        return self.execute_service_method('get_all_tasks')
    
    def get_task_by_id(self, task_id):
        """
        Получает задачу по ID
        """
        return self.execute_service_method('get_task_by_id', task_id)

    def get_tasks_by_developer(self, developer_id):
        """
        Получение списка задач, назначенных указанному разработчику

        Args:
            developer_id (int): ID разработчика

        Returns:
            dict: Результат операции с ключами:
                - success (bool): Успешность операции
                - data (list): Список объектов задач или None в случае ошибки
                - error_message (str): Сообщение об ошибке или None в случае успеха
        """
        try:
            from models import DBManager

            print(f"Получение задач для разработчика с ID: {developer_id}")

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

            # Запрос для получения задач разработчика с информацией о проекте и разработчике
            query = """
                SELECT t.id, t.project_id, t.developer_id, t.description, t.status, t.hours_worked,
                       t.created_at, t.updated_at, p.name as project_name, d.full_name as developer_name,
                       p.deadline as project_deadline
                FROM tasks t
                LEFT JOIN projects p ON t.project_id = p.id
                LEFT JOIN developers d ON t.developer_id = d.id
                WHERE t.developer_id = ?
            """

            db_manager.execute(query, (developer_id,))
            result = db_manager.fetch_all()

            print(f"Найдено задач для разработчика: {len(result) if result else 0}")

            if not result:
                # Проверяем, есть ли вообще задачи в базе
                db_manager.execute("SELECT COUNT(*) as count FROM tasks")
                count_result = db_manager.fetch_one()
                total_tasks = count_result['count'] if count_result else 0
                print(f"Всего задач в базе данных: {total_tasks}")

                return {
                    'success': True,
                    'data': [],
                    'error_message': None
                }

            # Преобразуем результаты в объекты Task
            from models.task import Task
            tasks = []
            for row in result:
                print(f"Обработка задачи: ID={row['id']}, Описание={row['description']}")
                task = Task(
                    id=row['id'],
                    project_id=row['project_id'],
                    developer_id=row['developer_id'],
                    description=row['description'],
                    status=row['status'],
                    hours_worked=row['hours_worked'],
                    created_at=row.get('created_at', ''),
                    updated_at=row.get('updated_at', '')
                )
                # Добавляем дополнительные атрибуты
                task.project_name = row['project_name']
                task.developer_name = row['developer_name']
                task.project_deadline = row['project_deadline']
                tasks.append(task)

            return {
                'success': True,
                'data': tasks,
                'error_message': None
            }
        except Exception as e:
            import traceback
            print(f"Ошибка при получении задач разработчика: {str(e)}")
            print(traceback.format_exc())
            return {
                'success': False,
                'data': None,
                'error_message': f"Ошибка при получении задач разработчика: {str(e)}"
            }

    def create_task(self, data):
        """
        Создает новую задачу
        """
        return self.execute_service_method('create_task', data)
    
    def update_task(self, task_id, data):
        """
        Обновляет данные задачи
        """
        return self.execute_service_method('update_task', task_id, data)
    
    def delete_task(self, task_id):
        """
        Удаляет задачу
        """
        return self.execute_service_method('delete_task', task_id)
    
    def assign_task(self, task_id, developer_id):
        """
        Назначает задачу разработчику
        """
        return self.execute_service_method('assign_task', task_id, developer_id)
    
    def update_task_status(self, task_id, status):
        """
        Обновляет статус задачи
        """
        return self.execute_service_method('update_task_status', task_id, status)
    
    def update_task_hours(self, task_id, hours):
        """
        Обновляет количество часов, затраченных на задачу
        """
        return self.execute_service_method('update_task_hours', task_id, hours)
    
    def search_tasks(self, search_term=None, project_id=None, developer_id=None, status=None):
        """
        Поиск задач по описанию, проекту, разработчику и/или статусу
        """
        return self.execute_service_method('search_tasks', search_term, project_id, developer_id, status)
    
    def get_task_statuses(self):
        """
        Получает список возможных статусов задач
        """
        return {
            'success': True,
            'data': ['новая', 'в работе', 'на проверке', 'завершено']
        }
