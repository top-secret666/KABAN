from services.base_service import BaseService
from models import User
from exceptions import BusinessException, ValidationException, DatabaseException
from datetime import datetime

class AuthService(BaseService):
    """
    Сервис для аутентификации и управления пользователями
    """

    def login(self, username, password):
        try:
            if not username or not password:
                raise ValidationException("Имя пользователя и пароль обязательны")

            # Получение пользователя по имени
            user = User.get_by_username(username, self.db_manager)
            if not user:
                raise BusinessException("Неверное имя пользователя или пароль")

            # Проверка активности пользователя
            if not user.is_active:
                raise BusinessException("Учетная запись отключена")

            # Для отладки: вывод информации о пользователе
            print(f"Найден пользователь: {user.username}, роль: {user.role}")
            print(f"Сохраненный пароль: {user.password}")
            print(f"Введенный пароль: {password}")

            # Проверка пароля
            if not user.check_password(password):
                raise BusinessException("Неверное имя пользователя или пароль")

            # Обновление времени последнего входа
            user.update_last_login()

            return user

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при аутентификации: {str(e)}")

    def register(self, username, password, email, full_name, role='developer'):
        """
        Регистрирует нового пользователя
        
        Args:
            username: Имя пользователя
            password: Пароль
            email: Email
            full_name: Полное имя
            role: Роль пользователя
        
        Returns:
            User: Созданный пользователь
        """
        try:
            # Проверка, что пользователь с таким именем не существует
            existing_user = User.get_by_username(username, self.db_manager)
            if existing_user:
                raise BusinessException(f"Пользователь с именем '{username}' уже существует")
            
            # Создание нового пользователя
            user = User(
                username=username,
                password=password,
                email=email,
                full_name=full_name,
                role=role,
                is_active=True,
                db_manager=self.db_manager
            )
            
            # Сохранение пользователя
            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось создать пользователя: {error}")
            
            return user
        
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при регистрации пользователя: {str(e)}")
    
    def get_user_by_id(self, user_id):
        """
        Получает пользователя по ID
        
        Args:
            user_id: ID пользователя
        
        Returns:
            User: Объект пользователя
        """
        try:
            user = User.get_by_id(user_id, self.db_manager)
            if not user:
                raise BusinessException(f"Пользователь с ID {user_id} не найден")
            return user
        
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении пользователя: {str(e)}")
    
    def get_all_users(self):
        """
        Получает список всех пользователей
        
        Returns:
            list: Список пользователей
        """
        try:
            return User.get_all(self.db_manager)
        
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка пользователей: {str(e)}")
    
    def update_user(self, user_id, data):
        """
        Обновляет данные пользователя
        
        Args:
            user_id: ID пользователя
            data: Словарь с обновляемыми данными
        
        Returns:
            User: Обновленный пользователь
        """
        try:
            # Получение пользователя
            user = self.get_user_by_id(user_id)
            
            # Обновление полей
            if 'username' in data:
                # Проверка уникальности имени пользователя
                if data['username'] != user.username:
                    existing_user = User.get_by_username(data['username'], self.db_manager)
                    if existing_user:
                        raise BusinessException(f"Пользователь с именем '{data['username']}' уже существует")
                user.username = data['username']
            
            if 'password' in data:
                user.password = data['password']
            
            if 'email' in data:
                user.email = data['email']
            
            if 'full_name' in data:
                user.full_name = data['full_name']
            
            if 'role' in data:
                user.role = data['role']
            
            if 'is_active' in data:
                user.is_active = data['is_active']
            
            # Сохранение изменений
            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось обновить пользователя: {error}")
            
            return user
        
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении пользователя: {str(e)}")
    
    def delete_user(self, user_id):
        """
        Удаляет пользователя
        
        Args:
            user_id: ID пользователя
        
        Returns:
            bool: Результат операции
        """
        try:
            # Получение пользователя
            user = self.get_user_by_id(user_id)
            
            # Удаление пользователя
            success, error = user.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить пользователя: {error}")
            
            return True
        
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении пользователя: {str(e)}")
    
    def change_password(self, user_id, old_password, new_password):
        """
        Изменяет пароль пользователя
        
        Args:
            user_id: ID пользователя
            old_password: Старый пароль
            new_password: Новый пароль
        
        Returns:
            bool: Результат операции
        """
        try:
            # Получение пользователя
            user = self.get_user_by_id(user_id)
            
            # Проверка старого пароля
            if not user.check_password(old_password):
                raise BusinessException("Неверный текущий пароль")
            
            # Установка нового пароля
            user.password = new_password
            
            # Сохранение изменений
            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось изменить пароль: {error}")
            
            return True
        
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при изменении пароля: {str(e)}")

    def reset_password(self, user_id, new_password):
        """
        Сбрасывает пароль пользователя (для администраторов)

        Args:
            user_id: ID пользователя
            new_password: Новый пароль

        Returns:
            bool: Результат операции
        """
        try:
            # Получение пользователя
            user = self.get_user_by_id(user_id)

            # Установка нового пароля
            user.password = new_password

            # Сохранение изменений
            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось сбросить пароль: {error}")

            return True

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при сбросе пароля: {str(e)}")