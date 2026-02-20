import sys
import os
import unittest
from datetime import datetime, timedelta

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DBManager
from models.notification import Notification
from services.notification_service import NotificationService
from controllers.notification_controller import NotificationController

class TestNotifications(unittest.TestCase):
    """
    Тесты для системы уведомлений
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
        sql_path = os.path.join(script_dir, 'database', 'kaban.sql')
        notifications_sql_path = os.path.join(script_dir, 'database', 'notifications.sql')
        
        cls.db_manager.connect()
        
        # Загружаем основной SQL-скрипт
        with open(sql_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            cls.db_manager.conn.executescript(sql_script)
        
        # Загружаем SQL-скрипт для уведомлений
        with open(notifications_sql_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            cls.db_manager.conn.executescript(sql_script)
        
        cls.db_manager.commit()
        
        # Создаем сервис и контроллер
        cls.notification_service = NotificationService(cls.db_manager)
        cls.notification_controller = NotificationController(cls.notification_service)
    
    def setUp(self):
        """
        Настройка перед каждым тестом
        """
        # Очищаем таблицу уведомлений перед каждым тестом
        self.db_manager.conn.execute("DELETE FROM notifications")
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
    
    def test_create_notification(self):
        """
        Тест создания уведомления
        """
        # Создание уведомления через сервис
        notification = self.notification_service.create_notification(
            title="Тестовое уведомление",
            message="Это тестовое уведомление",
            type="info"
        )
        
        # Проверка создания
        self.assertIsNotNone(notification)
        self.assertIsNotNone(notification.id)
        self.assertEqual(notification.title, "Тестовое уведомление")
        self.assertEqual(notification.message, "Это тестовое уведомление")
        self.assertEqual(notification.type, "info")
        self.assertFalse(notification.is_read)
        
        # Получение уведомления по ID
        retrieved = self.notification_service.get_notification_by_id(notification.id)
        self.assertEqual(retrieved.id, notification.id)
        self.assertEqual(retrieved.title, notification.title)
    
    def test_mark_as_read(self):
        """
        Тест отметки уведомления как прочитанного
        """
        # Создание уведомления
        notification = self.notification_service.create_notification(
            title="Тестовое уведомление",
            message="Это тестовое уведомление",
            type="info"
        )
        
        # Отметка как прочитанное
        result = self.notification_service.mark_as_read(notification.id)
        self.assertTrue(result)
        
        # Проверка статуса
        updated = self.notification_service.get_notification_by_id(notification.id)
        self.assertTrue(updated.is_read)
    
    def test_get_all_notifications(self):
        """
        Тест получения списка уведомлений
        """
        # Создание нескольких уведомлений
        self.notification_service.create_notification(
            title="Уведомление 1",
            message="Текст уведомления 1",
            type="info"
        )
        self.notification_service.create_notification(
            title="Уведомление 2",
            message="Текст уведомления 2",
            type="warning"
        )
        self.notification_service.create_notification(
            title="Уведомление 3",
            message="Текст уведомления 3",
            type="error"
        )
        
        # Получение всех уведомлений
        notifications = self.notification_service.get_all_notifications()
        self.assertEqual(len(notifications), 3)
        
        # Проверка типов уведомлений
        types = [n.type for n in notifications]
        self.assertIn("info", types)
        self.assertIn("warning", types)
        self.assertIn("error", types)
    
    def test_delete_notification(self):
        """
        Тест удаления уведомления
        """
        # Создание уведомления
        notification = self.notification_service.create_notification(
            title="Тестовое уведомление",
            message="Это тестовое уведомление",
            type="info"
        )
        
        # Удаление уведомления
        result = self.notification_service.delete_notification(notification.id)
        self.assertTrue(result)
        
        # Проверка удаления
        with self.assertRaises(Exception):
            self.notification_service.get_notification_by_id(notification.id)
    
    def test_notification_controller(self):
        """
        Тест контроллера уведомлений
        """
        # Создание уведомления через контроллер
        result = self.notification_controller.create_notification(
            title="Тестовое уведомление",
            message="Это тестовое уведомление",
            type="info"
        )
        
        # Проверка результата
        self.assertTrue(result['success'])
        notification = result['data']
        self.assertIsNotNone(notification.id)
        
        # Получение уведомления через контроллер
        get_result = self.notification_controller.get_notification_by_id(notification.id)
        self.assertTrue(get_result['success'])
        self.assertEqual(get_result['data'].id, notification.id)
        
        # Отметка как прочитанное через контроллер
        mark_result = self.notification_controller.mark_as_read(notification.id)
        self.assertTrue(mark_result['success'])
        
        # Удаление через контроллер
        delete_result = self.notification_controller.delete_notification(notification.id)
        self.assertTrue(delete_result['success'])
    
    def test_check_overdue_projects(self):
        """
        Тест проверки просроченных проектов
        """
        # Создаем проект с прошедшим дедлайном
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.db_manager.conn.execute(
            "INSERT INTO projects (name, client, deadline, budget) VALUES (?, ?, ?, ?)",
            ("Просроченный проект", "Тестовый клиент", yesterday, 100000)
        )
        self.db_manager.commit()
        
        # Запускаем проверку
        count = self.notification_service.check_overdue_projects()
        
        # Проверяем, что создано уведомление
        self.assertEqual(count, 1)
        
        # Проверяем содержимое уведомления
        notifications = self.notification_service.get_all_notifications()
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].type, "warning")
        self.assertIn("просрочен", notifications[0].message)
    
    def test_run_all_checks(self):
        """
        Тест запуска всех проверок
        """
        # Создаем тестовые данные для проверок
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        future = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
        
        # Просроченный проект
        self.db_manager.conn.execute(
            "INSERT INTO projects (name, client, deadline, budget) VALUES (?, ?, ?, ?)",
            ("Просроченный проект", "Тестовый клиент", yesterday, 100000)
        )
        
        # Проект с приближающимся дедлайном
        self.db_manager.conn.execute(
            "INSERT INTO projects (name, client, deadline, budget) VALUES (?, ?, ?, ?)",
            ("Скорый дедлайн", "Тестовый клиент", future, 100000)
        )
        
        self.db_manager.commit()
        
        # Запускаем все проверки
        result = self.notification_service.run_all_checks()
        
        # Проверяем результаты
        self.assertGreaterEqual(result['total'], 2)
        self.assertEqual(result['overdue_projects'], 1)
        self.assertEqual(result['upcoming_deadlines'], 1)

if __name__ == '__main__':
    unittest.main()
