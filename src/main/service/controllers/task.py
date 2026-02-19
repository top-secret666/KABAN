from src.main.service import TaskService


from .base import BaseController

class TaskController(BaseController):
    def __init__(self, service=None):
        self.service = service or TaskService()

    def get_all_tasks(self):
        return self.execute_service_method('get_all_tasks')

    def get_task_by_id(self, task_id):
        return self.execute_service_method('get_task_by_id', task_id)

    def create_task(self, data):
        return self.execute_service_method('create_task', data)

    def update_task(self, task_id, data):
        return self.execute_service_method('update_task', task_id, data)

    def delete_task(self, task_id):
        return self.execute_service_method('delete_task', task_id)

    def assign_task(self, task_id, developer_id):
        return self.execute_service_method('assign_task', task_id, developer_id)

    def update_task_status(self, task_id, status):
        return self.execute_service_method('update_task_status', task_id, status)

    def update_task_hours(self, task_id, hours):
        return self.execute_service_method('update_task_hours', task_id, hours)

    def search_tasks(self, search_term=None, project_id=None, developer_id=None, status=None):
        return self.execute_service_method('search_tasks', search_term, project_id, developer_id, status)

    def get_task_statuses(self):
        return {
            'success': True,
            'data': ['новая', 'в работе', 'на проверке', 'завершено']
        }
