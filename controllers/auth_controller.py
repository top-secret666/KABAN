from controllers.base_controller import BaseController
from services.auth_service import AuthService

class AuthController(BaseController):
    """
    Контроллер для аутентификации и управления пользователями
    """
    def __init__(self, service=None):
        """
        Инициализирует контроллер с сервисом аутентификации
        """
        super().__init__(service or AuthService())
    
    def login(self, username, password):
        """
        Аутентифицирует пользователя
        """
        return self.execute_service_method('login', username, password)
    
    def register(self, username, password, email, full_name, role='developer'):
        """
        Регистрирует нового пользователя
        """
        return self.execute_service_method('register', username, password, email, full_name, role)
    
    def get_user_by_id(self, user_id):
        """
        Получает пользователя по ID
        """
        return self.execute_service_method('get_user_by_id', user_id)

    def get_all_users(self):
        """
        Получает список всех пользователей

        Returns:
            dict: Словарь с результатом операции
        """
        try:
            users = self.service.get_all_users()
            return {'success': True, 'data': users}
        except Exception as e:
            return {'success': False, 'error_message': str(e)}

    def update_user(self, user_id, data):
        """
        Обновляет данные пользователя
        """
        return self.execute_service_method('update_user', user_id, data)
    
    def delete_user(self, user_id):
        """
        Удаляет пользователя
        """
        return self.execute_service_method('delete_user', user_id)
    
    def change_password(self, user_id, old_password, new_password):
        """
        Изменяет пароль пользователя
        """
        return self.execute_service_method('change_password', user_id, old_password, new_password)

    def reset_password(self, user_id, new_password):
        """
        Сбрасывает пароль пользователя (для администраторов)
        """
        return self.execute_service_method('reset_password', user_id, new_password)