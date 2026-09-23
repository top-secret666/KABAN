import sys
import os
import unittest
from datetime import datetime, timedelta

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Developer, Project, Task, DBManager

class TestModels(unittest.TestCase):
    """
    Тесты для моделей данных
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
    
    def test_developer_model(self):
        """
        Тест модели разработчика
        """
        # Создание разработчика
        developer = Developer(
            full_name="Тестовый Разработчик",
            position="backend",
            hourly_rate=1000
        )
        
        # Валидация
        is_valid, error_message = developer.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
        
        # Сохранение
        success, error = developer.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(developer.id)
        
        # Получение по ID
        retrieved_developer = Developer.get_by_id(developer.id)
        self.assertIsNotNone(retrieved_developer)
        self.assertEqual(retrieved_developer.full_name, "Тестовый Разработчик")
        self.assertEqual(retrieved_developer.position, "backend")
        self.assertEqual(retrieved_developer.hourly_rate, 1000)
        
        # Обновление
        developer.full_name = "Обновленный Разработчик"
        success, error = developer.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка обновления
        updated_developer = Developer.get_by_id(developer.id)
        self.assertEqual(updated_developer.full_name, "Обновленный Разработчик")
        
        # Удаление
        success, error = developer.delete()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка удаления
        deleted_developer = Developer.get_by_id(developer.id)
        self.assertIsNone(deleted_developer)
    
    def test_project_model(self):
        """
        Тест модели проекта
        """
        # Создание проекта
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project = Project(
            name="Тестовый Проект",
            client="Тестовый Клиент",
            deadline=deadline,
            budget=100000
        )
        
        # Валидация
        is_valid, error_message = project.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
        
        # Сохранение
        success, error = project.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(project.id)
        
        # Получение по ID
        retrieved_project = Project.get_by_id(project.id)
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.name, "Тестовый Проект")
        self.assertEqual(retrieved_project.client, "Тестовый Клиент")
        self.assertEqual(retrieved_project.deadline, deadline)
        self.assertEqual(retrieved_project.budget, 100000)
        
        # Обновление
        project.name = "Обновленный Проект"
        success, error = project.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка обновления
        updated_project = Project.get_by_id(project.id)
        self.assertEqual(updated_project.name, "Обновленный Проект")
        
        # Удаление
        success, error = project.delete()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка удаления
        deleted_project = Project.get_by_id(project.id)
        self.assertIsNone(deleted_project)
    
    def test_task_model(self):
        """
        Тест модели задачи
        """
        # Создание разработчика и проекта для задачи
        developer = Developer(
            full_name="Тестовый Разработчик",
            position="backend",
            hourly_rate=1000
        )
        developer.save()
        
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project = Project(
            name="Тестовый Проект",
            client="Тестовый Клиент",
            deadline=deadline,
            budget=100000
        )
        project.save()
        
        # Создание задачи
        task = Task(
            project_id=project.id,
            developer_id=developer.id,
            description="Тестовая Задача",
            status="в работе",
            hours_worked=5
        )
        
        # Валидация
        is_valid, error_message = task.validate()
        self.assertTrue(is_valid)
        self.assertIsNone(error_message)
        
        # Сохранение
        success, error = task.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertIsNotNone(task.id)
        
        # Получение по ID
        retrieved_task = Task.get_by_id(task.id)
        self.assertIsNotNone(retrieved_task)
        self.assertEqual(retrieved_task.project_id, project.id)
        self.assertEqual(retrieved_task.developer_id, developer.id)
        self.assertEqual(retrieved_task.description, "Тестовая Задача")
        self.assertEqual(retrieved_task.status, "в работе")
        self.assertEqual(retrieved_task.hours_worked, 5)
        
        # Обновление
        task.description = "Обновленная Задача"
        success, error = task.save()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка обновления
        updated_task = Task.get_by_id(task.id)
        self.assertEqual(updated_task.description, "Обновленная Задача")
        
        # Обновление статуса
        success, error = task.update_status("завершено")
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка обновления статуса
        updated_task = Task.get_by_id(task.id)
        self.assertEqual(updated_task.status, "завершено")
        
        # Обновление часов
        success, error = task.update_hours(10)
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка обновления часов
        updated_task = Task.get_by_id(task.id)
        self.assertEqual(updated_task.hours_worked, 10)
        
        # Получение связанных объектов
        project_obj = task.get_project()
        self.assertIsNotNone(project_obj)
        self.assertEqual(project_obj.id, project.id)
        
        developer_obj = task.get_developer()
        self.assertIsNotNone(developer_obj)
        self.assertEqual(developer_obj.id, developer.id)
        
        # Удаление
        success, error = task.delete()
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Проверка удаления
        deleted_task = Task.get_by_id(task.id)
        self.assertIsNone(deleted_task)
        
        # Очистка
        developer.delete()
        project.delete()
    
    def test_relationships(self):
        """
        Тест связей между моделями
        """
        # Создание разработчика и проекта
        developer = Developer(
            full_name="Тестовый Разработчик",
            position="backend",
            hourly_rate=1000
        )
        developer.save()
        
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project = Project(
            name="Тестовый Проект",
            client="Тестовый Клиент",
            deadline=deadline,
            budget=100000
        )
        project.save()
        
        # Создание задач
        task1 = Task(
            project_id=project.id,
            developer_id=developer.id,
            description="Задача 1",
            status="в работе",
            hours_worked=5
        )
        task1.save()
        
        task2 = Task(
            project_id=project.id,
            developer_id=developer.id,
            description="Задача 2",
            status="завершено",
            hours_worked=3
        )
        task2.save()
        
        # Получение задач проекта
        project_tasks = project.get_tasks()
        self.assertEqual(len(project_tasks), 2)
        
        # Получение задач разработчика
        developer_tasks = developer.get_tasks()
        self.assertEqual(len(developer_tasks), 2)
        
        # Расчет зарплаты разработчика
        salary = developer.calculate_salary()
        self.assertEqual(salary, 8000)  # 8 часов * 1000 руб/час
        
        # Получение прогресса проекта
        progress = project.get_progress()
        self.assertEqual(progress['total_tasks'], 2)
        self.assertEqual(progress['completed_tasks'], 1)
        self.assertEqual(progress['progress_percent'], 50.0)
        self.assertEqual(progress['total_hours'], 8)
        
        # Очистка
        task1.delete()
        task2.delete()
        developer.delete()
        project.delete()

if __name__ == '__main__':
    unittest.main()
