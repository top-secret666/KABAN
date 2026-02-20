import sys
import os
import unittest
from datetime import datetime, timedelta

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import DBManager
from controllers import DeveloperController, ProjectController, TaskController, ReportController
from exceptions import ValidationException

class TestControllers(unittest.TestCase):
    """
    Тесты для контроллеров
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
        
        # Создаем контроллеры
        cls.developer_controller = DeveloperController()
        cls.project_controller = ProjectController()
        cls.task_controller = TaskController()
        cls.report_controller = ReportController()

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

    def test_developer_controller(self):
        """
        Тест контроллера разработчиков
        """
        # Получение списка должностей
        positions_result = self.developer_controller.get_developer_positions()
        self.assertTrue(positions_result['success'])
        self.assertIn('frontend', positions_result['data'])
        
        # Создание разработчика
        developer_data = {
            'full_name': 'Тестовый Разработчик',
            'position': 'backend',
            'hourly_rate': 1000
        }
        create_result = self.developer_controller.create_developer(developer_data)
        self.assertTrue(create_result['success'])
        self.assertIsNotNone(create_result['data'].id)
        developer_id = create_result['data'].id
        
        # Получение разработчика по ID
        get_result = self.developer_controller.get_developer_by_id(developer_id)
        self.assertTrue(get_result['success'])
        self.assertEqual(get_result['data'].full_name, 'Тестовый Разработчик')
        
        # Обновление разработчика
        update_data = {
            'full_name': 'Обновленный Разработчик',
            'position': 'frontend',
            'hourly_rate': 1200
        }
        update_result = self.developer_controller.update_developer(developer_id, update_data)
        self.assertTrue(update_result['success'])
        self.assertEqual(update_result['data'].full_name, 'Обновленный Разработчик')
        
        # Поиск разработчиков
        search_result = self.developer_controller.search_developers(search_term='Обновленный')
        self.assertTrue(search_result['success'])
        self.assertGreaterEqual(len(search_result['data']), 1)
        
        # Удаление разработчика
        delete_result = self.developer_controller.delete_developer(developer_id)
        self.assertTrue(delete_result['success'])
        
        # Проверка обработки ошибок
        invalid_data = {
            'full_name': '',  # Пустое имя должно вызвать ошибку валидации
            'position': 'backend',
            'hourly_rate': 1000
        }
        error_result = self.developer_controller.create_developer(invalid_data)
        self.assertFalse(error_result['success'])
        self.assertEqual(error_result['error_type'], 'Ошибка валидации')

    def test_project_controller(self):
        """
        Тест контроллера проектов
        """
        # Создание проекта
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project_data = {
            'name': 'Тестовый Проект',
            'client': 'Тестовый Клиент',
            'deadline': deadline,
            'budget': 100000
        }
        create_result = self.project_controller.create_project(project_data)
        self.assertTrue(create_result['success'])
        self.assertIsNotNone(create_result['data'].id)
        project_id = create_result['data'].id
        
        # Получение проекта по ID
        get_result = self.project_controller.get_project_by_id(project_id)
        self.assertTrue(get_result['success'])
        self.assertEqual(get_result['data'].name, 'Тестовый Проект')
        
        # Обновление проекта
        update_data = {
            'name': 'Обновленный Проект',
            'client': 'Обновленный Клиент',
            'budget': 150000
        }
        update_result = self.project_controller.update_project(project_id, update_data)
        self.assertTrue(update_result['success'])
        self.assertEqual(update_result['data'].name, 'Обновленный Проект')
        
        # Поиск проектов
        search_result = self.project_controller.search_projects(search_term='Обновленный')
        self.assertTrue(search_result['success'])
        self.assertGreaterEqual(len(search_result['data']), 1)
        
        # Получение прогресса проекта
        progress_result = self.project_controller.get_project_progress(project_id)
        self.assertTrue(progress_result['success'])
        
        # Удаление проекта
        delete_result = self.project_controller.delete_project(project_id)
        self.assertTrue(delete_result['success'])
        
        # Проверка обработки ошибок
        invalid_data = {
            'name': '',  # Пустое название должно вызвать ошибку валидации
            'client': 'Тестовый Клиент',
            'deadline': deadline,
            'budget': 100000
        }
        error_result = self.project_controller.create_project(invalid_data)
        self.assertFalse(error_result['success'])
        self.assertEqual(error_result['error_type'], 'Ошибка валидации')

    def test_task_controller(self):
        """
        Тест контроллера задач
        """
        # Получение списка статусов
        statuses_result = self.task_controller.get_task_statuses()
        self.assertTrue(statuses_result['success'])
        self.assertIn('новая', statuses_result['data'])
        
        # Создание разработчика и проекта для задачи
        developer_data = {
            'full_name': 'Тестовый Разработчик',
            'position': 'backend',
            'hourly_rate': 1000
        }
        developer_result = self.developer_controller.create_developer(developer_data)
        developer_id = developer_result['data'].id
        
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project_data = {
            'name': 'Тестовый Проект',
            'client': 'Тестовый Клиент',
            'deadline': deadline,
            'budget': 100000
        }
        project_result = self.project_controller.create_project(project_data)
        project_id = project_result['data'].id
        
        # Создание задачи
        task_data = {
            'project_id': project_id,
            'developer_id': developer_id,
            'description': 'Тестовая Задача',
            'status': 'новая',
            'hours_worked': 0
        }
        create_result = self.task_controller.create_task(task_data)
        self.assertTrue(create_result['success'])
        self.assertIsNotNone(create_result['data'].id)
        task_id = create_result['data'].id
        
        # Получение задачи по ID
        get_result = self.task_controller.get_task_by_id(task_id)
        self.assertTrue(get_result['success'])
        self.assertEqual(get_result['data'].description, 'Тестовая Задача')
        
        # Обновление задачи
        update_data = {
            'description': 'Обновленная Задача',
            'status': 'в работе',
            'hours_worked': 5
        }
        update_result = self.task_controller.update_task(task_id, update_data)
        self.assertTrue(update_result['success'])
        self.assertEqual(update_result['data'].description, 'Обновленная Задача')
        
        # Обновление статуса задачи
        status_result = self.task_controller.update_task_status(task_id, 'завершено')
        self.assertTrue(status_result['success'])
        self.assertEqual(status_result['data'].status, 'завершено')
        
        # Обновление часов задачи
        hours_result = self.task_controller.update_task_hours(task_id, 10)
        self.assertTrue(hours_result['success'])
        self.assertEqual(hours_result['data'].hours_worked, 10)
        
        # Поиск задач
        search_result = self.task_controller.search_tasks(search_term='Обновленная')
        self.assertTrue(search_result['success'])
        self.assertGreaterEqual(len(search_result['data']), 1)
        
        # Удаление задачи
        delete_result = self.task_controller.delete_task(task_id)
        self.assertTrue(delete_result['success'])
        
        # Очистка
        self.developer_controller.delete_developer(developer_id)
        self.project_controller.delete_project(project_id)
        
        # Проверка обработки ошибок
        invalid_data = {
            'project_id': 9999,  # Несуществующий проект должен вызвать ошибку
            'description': 'Тестовая Задача',
            'status': 'новая',
            'hours_worked': 0
        }
        error_result = self.task_controller.create_task(invalid_data)
        self.assertFalse(error_result['success'])
        self.assertEqual(error_result['error_type'], 'Ошибка бизнес-логики')

    def test_report_controller(self):
        """
        Тест контроллера отчетов
        """
        # Создание тестовых данных
        developer_data = {
            'full_name': 'Тестовый Разработчик',
            'position': 'backend',
            'hourly_rate': 1000
        }
        developer_result = self.developer_controller.create_developer(developer_data)
        developer_id = developer_result['data'].id
        
        deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        project_data = {
            'name': 'Тестовый Проект',
            'client': 'Тестовый Клиент',
            'deadline': deadline,
            'budget': 100000
        }
        project_result = self.project_controller.create_project(project_data)
        project_id = project_result['data'].id
        
        task_data = {
            'project_id': project_id,
            'developer_id': developer_id,
            'description': 'Тестовая Задача',
            'status': 'в работе',
            'hours_worked': 5
        }
        self.task_controller.create_task(task_data)
        
        # Получение отчета по статусу проектов
        project_status_result = self.report_controller.get_project_status_report()
        self.assertTrue(project_status_result['success'])
        self.assertIn('projects', project_status_result['data'])
        
        # Получение отчета по загрузке разработчиков
        workload_result = self.report_controller.get_developer_workload_report()
        self.assertTrue(workload_result['success'])
        self.assertIn('developers', workload_result['data'])
        
        # Экспорт отчета в CSV
        import tempfile
        temp_dir = tempfile.gettempdir()
        csv_filename = os.path.join(temp_dir, 'test_report.csv')
        
        export_result = self.report_controller.export_report_to_csv(
            workload_result['data'], 
            csv_filename
        )
        self.assertTrue(export_result['success'])
        self.assertTrue(os.path.exists(csv_filename))
        
        # Очистка
        os.remove(csv_filename)
        self.task_controller.delete_task(1)  # Предполагаем, что ID задачи = 1
        self.developer_controller.delete_developer(developer_id)
        self.project_controller.delete_project(project_id)

if __name__ == '__main__':
    unittest.main()
