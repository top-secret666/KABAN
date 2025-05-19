import logging
from .auth_service import AuthService
from src.main.service.exceptions import BusinessException, ValidationException, DatabaseException

class AuthController:
    def __init__(self, service=None, db_manager=None):
        self.service = service or AuthService(db_manager)
        self.logger = logging.getLogger()

    def execute_service_method(self, method_name, *args, **kwargs):
        try:
            method = getattr(self.service, method_name)
            result = method(*args, **kwargs)
            return {'success': True, 'data': result}
        except Exception as e:
            import logging
            logging.error(f"Ошибка в {method_name}: {str(e)}")
            return {'success': False, 'error_message': str(e)}

    def login(self, username, password):
        return self.execute_service_method('login', username, password)

    def register(self, username, password, email, full_name, role='developer'):
        return self.execute_service_method('register', username, password, email, full_name, role)

    def get_user_by_id(self, user_id):
        return self.execute_service_method('get_user_by_id', user_id)

    def get_all_users(self):
        return self.execute_service_method('get_all_users')

    def update_user(self, user_id, data):
        return self.execute_service_method('update_user', user_id, data)

    def delete_user(self, user_id):
        return self.execute_service_method('delete_user', user_id)

    def change_password(self, user_id, old_password, new_password):
        return self.execute_service_method('change_password', user_id, old_password, new_password)
