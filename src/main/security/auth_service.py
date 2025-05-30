from src.main.models import User
from src.main.service.exceptions import BusinessException, ValidationException, DatabaseException


class AuthService:
    def __init__(self, db_manager=None):
        # Initialize db_manager in the constructor
        self.db_manager = db_manager

    def login(self, username, password):
        try:
            if not username or not password:
                raise ValidationException("Имя пользователя и пароль обязательны")

            user = User.get_by_username(username, self.db_manager)
            if not user:
                raise BusinessException("Неверное имя пользователя или пароль")

            if not user.is_active:
                raise BusinessException("Учетная запись отключена")

            if not user.check_password(password):
                raise BusinessException("Неверное имя пользователя или пароль")

            user.update_last_login()

            return user

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при аутентификации: {str(e)}")

    def register(self, username, password, email, full_name, role='developer'):
        try:
            existing_user = User.get_by_username(username, self.db_manager)
            if existing_user:
                raise BusinessException(f"Пользователь с именем '{username}' уже существует")

            user = User(
                username=username,
                password=password,
                email=email,
                full_name=full_name,
                role=role,
                is_active=True,
                db_manager=self.db_manager
            )

            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось создать пользователя: {error}")

            return user

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при регистрации пользователя: {str(e)}")

    def get_user_by_id(self, user_id):
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
        try:
            return User.get_all(self.db_manager)

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка пользователей: {str(e)}")

    def update_user(self, user_id, data):
        try:
            user = self.get_user_by_id(user_id)

            if 'username' in data:
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

            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось обновить пользователя: {error}")

            return user

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении пользователя: {str(e)}")

    def delete_user(self, user_id):
        try:
            user = self.get_user_by_id(user_id)

            success, error = user.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить пользователя: {error}")

            return True

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении пользователя: {str(e)}")

    def change_password(self, user_id, old_password, new_password):
        try:
            user = self.get_user_by_id(user_id)

            if not user.check_password(old_password):
                raise BusinessException("Неверный текущий пароль")

            user.password = new_password

            success, error = user.save()
            if not success:
                raise BusinessException(f"Не удалось изменить пароль: {error}")

            return True

        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при изменении пароля: {str(e)}")
