from controllers.base_controller import BaseController
from services import DeveloperService

class DeveloperController(BaseController):
    """
    Контроллер для управления разработчиками
    """
    def __init__(self, service=None):
        """
        Инициализирует контроллер с сервисом разработчиков
        """
        super().__init__(service or DeveloperService())
    
    def get_all_developers(self):
        """
        Получает список всех разработчиков
        """
        return self.execute_service_method('get_all_developers')
    
    def get_developer_by_id(self, developer_id):
        """
        Получает разработчика по ID
        """
        return self.execute_service_method('get_developer_by_id', developer_id)
    
    def create_developer(self, data):
        """
        Создает нового разработчика
        """
        return self.execute_service_method('create_developer', data)
    
    def update_developer(self, developer_id, data):
        """
        Обновляет данные разработчика
        """
        return self.execute_service_method('update_developer', developer_id, data)
    
    def delete_developer(self, developer_id):
        """
        Удаляет разработчика
        """
        return self.execute_service_method('delete_developer', developer_id)
    
    def search_developers(self, search_term=None, position=None):
        """
        Поиск разработчиков по имени и/или должности
        """
        return self.execute_service_method('search_developers', search_term, position)
    
    def calculate_developer_salary(self, developer_id, start_date=None, end_date=None):
        """
        Расчет зарплаты разработчика за период
        """
        return self.execute_service_method('calculate_developer_salary', developer_id, start_date, end_date)
    
    def get_developer_positions(self):
        """
        Получает список возможных должностей разработчиков
        """
        return {
            'success': True,
            'data': ['frontend', 'backend', 'fullstack', 'designer', 'tester', 'manager']
        }
