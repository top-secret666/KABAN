import sys
import os
import unittest

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DBManager, User
from services.auth_service import AuthService
from controllers.auth_controller import AuthController
from exceptions import BusinessException

class TestAuth(unittest.TestCase):
    """
    Тесты для системы аутентификации
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Настройка перед всеми тестами
        """
        # Используем временную базу данных для тестов
        cls.db_manager = DBManager(':memory:')
        
        # Инициализируем базу данных
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        auth_sql_path = os.path.join(script_dir, 'database', 'auth.sql')
        
        cls.db_manager.connect()
        
        # Загружаем SQL-скрипт для аутентификации
        with open(auth_sql_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            cls.db_manager.conn.executescript(sql_script)
        
        cls.db_manager.commit()
        
        # Создаем сервис и контроллер
        cls.auth_service = AuthService(cls.db_manager)
        cls.auth_controller = AuthController(cls.auth_service)
    
    def setUp(self):
        """
        Настройка перед каждым тестом
        """
        # Очищаем таблицу пользователей перед каждым тестом, кроме администратора
        self.db_manager.conn.execute("DELETE FROM users WHERE username != 'admin'")
        self.db_manager.commit()
    
    def tearDown(self):
        """
        Очистка после каждого теста
        """
        pass
    
    @classmethod
    def tearDownClass(cls):
        """
        Очистка после всех тестов
        """
        cls.db_manager.close()
    
    def test_user_model(self):
        """
        Тест модели пользователя
        """
        # Создание пользователя
        user = User(
            username="testuser",
            password="password123",
            email="test@example.com",
            full_name="Test User",
            role="developer",
            db_manager=self.db_manager
        )
        
        # Валидация
        is_valid, error_message = user.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
        
        # Сохранение
        success, error = user.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(user.id)
        
        # Проверка хеширования пароля
        self.assertTrue(user.password.startswith('$'))
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrongpassword"))
        
        # Получение по ID
        retrieved_user = User.get_by_id(user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.email, "test@example.com")
        
        # Получение по имени пользователя
        retrieved_user = User.get_by_username("testuser")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, user.id)
        
        # Обновление
        user.full_name = "Updated User"
        success, error = user.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка обновления
        updated_user = User.get_by_id(user.id)
        self.assertEqual(updated_user.full_name, "Updated User")
        
        # Обновление последнего входа
        success, error = user.update_last_login()
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(user.last_login)
        
        # Удаление
        success, error = user.delete()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка удаления
        deleted_user = User.get_by_id(user.id)
        self.assertIsNone(deleted_user)
    
    def test_auth_service(self):
        """
        Тест сервиса аутентификации
        """
        # Регистрация пользователя
        user = self.auth_service.register(
            username="testuser",
            password="password123",
            email="test@example.com",
            full_name="Test User",
            role="developer"
        )
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        
        # Попытка регистрации с существующим именем пользователя
        with self.assertRaises(BusinessException):
            self.auth_service.register(
                username="testuser",
                password="password456",
                email="another@example.com",
                full_name="Another User",
                role="developer"
            )
        
        # Вход с правильными учетными данными
        logged_in_user = self.auth_service.login("testuser", "password123")
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.id, user.id)
        
        # Вход с неправильным паролем
        with self.assertRaises(BusinessException):
            self.auth_service.login("testuser", "wrongpassword")
        
        # Вход с несуществующим пользователем
        with self.assertRaises(BusinessException):
            self.auth_service.login("nonexistent", "password123")
        
        # Получение пользователя по ID
        retrieved_user = self.auth_service.get_user_by_id(user.id)
        self.assertEqual(retrieved_user.username, "testuser")
        
        # Получение всех пользователей
        all_users = self.auth_service.get_all_users()
        self.assertGreaterEqual(len(all_users), 2)  # admin + testuser
        
        # Обновление пользователя
        updated_user = self.auth_service.update_user(user.id, {
            'full_name': 'Updated User',
            'email': 'updated@example.com'
        })
        self.assertEqual(updated_user.full_name, 'Updated User')
        self.assertEqual(updated_user.email, 'updated@example.com')
        
        # Изменение пароля
        success = self.auth_service.change_password(user.id, "password123", "newpassword")
        self.assertTrue(success)
        
        # Вход с новым паролем
        logged_in_user = self.auth_service.login("testuser", "newpassword")
        self.assertIsNotNone(logged_in_user)
        
        # Удаление пользователя
        success = self.auth_service.delete_user(user.id)
        self.assertTrue(success)
        
        # Проверка удаления
        with self.assertRaises(BusinessException):
            self.auth_service.get_user_by_id(user.id)
    
    def test_auth_controller(self):
        """
        Тест контроллера аутентификации
        """
        # Регистрация пользователя через контроллер
        register_result = self.auth_controller.register(
            username="testuser",
            password="password123",
            email="test@example.com",
            full_name="Test User",
            role="developer"
        )
        self.assertTrue(register_result['success'])
        user = register_result['data']
        
        # Вход через контроллер
        login_result = self.auth_controller.login("testuser", "password123")
        self.assertTrue(login_result['success'])
        
        # Получение пользователя через контроллер
        get_result = self.auth_controller.get_user_by_id(user.id)
        self.assertTrue(get_result['success'])
        
        # Получение всех пользователей через контроллер
        all_result = self.auth_controller.get_all_users()
        self.assertTrue(all_result['success'])
        
        # Обновление пользователя через контроллер
        update_result = self.auth_controller.update_user(user.id, {
            'full_name': 'Updated User'
        })
        self.assertTrue(update_result['success'])
        
        # Изменение пароля через контроллер
        change_result = self.auth_controller.change_password(
            user.id, "password123", "newpassword"
        )
        self.assertTrue(change_result['success'])
        
        # Удаление пользователя через контроллер
        delete_result = self.auth_controller.delete_user(user.id)
        self.assertTrue(delete_result['success'])

if __name__ == '__main__':
    unittest.main()
