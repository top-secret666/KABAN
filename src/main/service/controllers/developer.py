from src.main.service import DeveloperService


from .base import BaseController

class DeveloperController(BaseController):
    def __init__(self, service=None):
        self.service = service or DeveloperService()

    def get_all_developers(self):
        return self.execute_service_method('get_all_developers')

    def get_developer_by_id(self, developer_id):
        return self.execute_service_method('get_developer_by_id', developer_id)

    def create_developer(self, data):
        return self.execute_service_method('create_developer', data)

    def update_developer(self, developer_id, data):
        return self.execute_service_method('update_developer', developer_id, data)

    def delete_developer(self, developer_id):
        return self.execute_service_method('delete_developer', developer_id)

    def search_developers(self, search_term=None, position=None):
        return self.execute_service_method('search_developers', search_term, position)

    def calculate_developer_salary(self, developer_id, start_date=None, end_date=None):
        return self.execute_service_method('calculate_developer_salary', developer_id, start_date, end_date)

    def get_developer_positions(self):
        return {
            'success': True,
            'data': ['frontend', 'backend', 'fullstack', 'designer', 'tester', 'manager']
        }
