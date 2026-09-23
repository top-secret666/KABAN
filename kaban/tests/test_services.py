import sys
import os
import unittest
from datetime import datetime, timedelta

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DBManager, Developer, Project, Task
from services import DeveloperService, ProjectService, TaskService, ReportService
from exceptions import ValidationException, BusinessException

class TestServices(unittest.TestCase):
    """
    Тесты для сервисов
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
        
        with open(sql_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        
        cls.db_manager.connect()
        cls.db_manager.conn.executescript(sql_script)
        cls.db_manager.commit()
        
        # Создаем сервисы
        cls.developer_service = DeveloperService(cls.db_manager)
        cls.project_service = ProjectService(cls.db_manager)
        cls.task_service = TaskService(cls.db_manager)
        cls.report_service = ReportService(cls.db_manager)

    def setUp(self):
        """
        Настройка перед каждым тестом
        """
        pass

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

    def test_developer_service(self):
        """
        Тест сервиса разработчиков
        """
        # Создание разработчика
        developer_data = {
            'full_name': 'Тестовый Разработчик',
            'position': 'backend',
            'hourly_rate': 1000
        }
        developer = self.developer_service.create_developer(developer_data)
        self.assertIsNotNone(developer)
        self.assertIsNotNone(developer.id)
        
        # Получение разработчика по ID
        retrieved_developer = self.developer_service.get_developer_by_id(developer.id)
        self.assertIsNotNone(retrieved_developer)
        self.assertEqual(retrieved_developer.full_name, 'Тестовый Разработчик')
        
        # Обновление разработчика
        update_data = {
            'full_name': 'Обновленный Разработчик',
            'position': 'frontend',
            'hourly_rate': 1200
        }
        updated_developer = self.developer_service.update_developer(developer.id, update_data)
        self.assertEqual(updated_developer.full_name, 'Обновленный Разработчик')
        self.assertEqual(updated_developer.position, 'frontend')
        self.assertEqual(updated_developer.hourly_rate, 1200)
        
        # Поиск разработчиков
        developers = self.developer_service.search_developers(search_term='Обновленный')
        self.assertGreaterEqual(len(developers), 1)
        
        # Удаление разработчика
        result = self.developer_service.delete_developer(developer.id)
        self.assertTrue(result)
        
        # Проверка удаления
        with self.assertRaises(BusinessException):
            self.developer_service.get_developer_by_id(developer.id)

    def test_project_service(self):
        """
        Тест сервиса проектов
        """
        # Создание проекта
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project_data = {
            'name': 'Тестовый Проект',
            'client': 'Тестовый Клиент',
            'deadline': deadline,
            'budget': 100000
        }
        project = self.project_service.create_project(project_data)
        self.assertIsNotNone(project)
        self.assertIsNotNone(project.id)
        
        # Получение проекта по ID
        retrieved_project = self.project_service.get_project_by_id(project.id)
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.name, 'Тестовый Проект')
        
        # Обновление проекта
        update_data = {
            'name': 'Обновленный Проект',
            'client': 'Обновленный Клиент',
            'budget': 150000
        }
        updated_project = self.project_service.update_project(project.id, update_data)
        self.assertEqual(updated_project.name, 'Обновленный Проект')
        self.assertEqual(updated_project.client, 'Обновленный Клиент')
        self.assertEqual(updated_project.budget, 150000)
        
        # Поиск проектов
        projects = self.project_service.search_projects(search_term='Обновленный')
        self.assertGreaterEqual(len(projects), 1)
        
        # Получение прогресса проекта
        progress = self.project_service.get_project_progress(project.id)
        self.assertIsNotNone(progress)
        
        # Удаление проекта
        result = self.project_service.delete_project(project.id)
        self.assertTrue(result)
        
        # Проверка удаления
        with self.assertRaises(BusinessException):
            self.project_service.get_project_by_id(project.id)

    def test_task_service(self):
        """
        Тест сервиса задач
        """
        # Создание разработчика и проекта для задачи
        developer_data = {
            'full_name': 'Тестовый Разработчик',
            'position': 'backend',
            'hourly_rate': 1000
        }
        developer = self.developer_service.create_developer(developer_data)
        
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project_data = {
            'name': 'Тестовый Проект',
            'client': 'Тестовый Клиент',
            'deadline': deadline,
            'budget': 100000
        }
        project = self.project_service.create_project(project_data)
        
        # Создание задачи
        task_data = {
            'project_id': project.id,
            'developer_id': developer.id,
            'description': 'Тестовая Задача',
            'status': 'в работе',
            'hours_worked': 0
        }
        task = self.task_service.create_task(task_data)
        self.assertIsNotNone(task)
        self.assertIsNotNone(task.id)
        
        # Получение задачи по ID
        retrieved_task = self.task_service.get_task_by_id(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.description, 'Тестовая Задача')
        
        # Обновление задачи
        update_data = {
            'description': 'Обновленная Задача',
            'status': 'в работе',
            'hours_worked': 5
        }
        updated_task = self.task_service.update_task(task.id, update_data)
        self.assertEqual(updated_task.description, 'Обновленная Задача')
        self.assertEqual(updated_task.status, 'в работе')
        self.assertEqual(updated_task.hours_worked, 5)
        
        # Обновление статуса задачи
        status_task = self.task_service.update_task_status(task.id, 'завершено')
        self.assertEqual(status_task.status, 'завершено')
        
        # Обновление часов зад

