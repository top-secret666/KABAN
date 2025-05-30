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
