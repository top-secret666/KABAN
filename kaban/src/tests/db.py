import sqlite3
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.init_db import init_database


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_path = ':memory:'

        src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_root = os.path.dirname(src_dir)
        sql_path = os.path.join(project_root, 'database', 'kaban.sql')

        if not os.path.exists(sql_path):
            raise FileNotFoundError(f"SQL файл не найден по пути: {sql_path}")

        cls.conn = sqlite3.connect(cls.db_path)
        cls.conn.row_factory = sqlite3.Row

        with open(sql_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
            cls.conn.executescript(sql_script)

        print(f"База данных успешно инициализирована: {cls.db_path}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'conn') and cls.conn:
            cls.conn.close()

    def setUp(self):
        self.cursor = self.__class__.conn.cursor()

    def tearDown(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()

    def test_tables_exist(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cursor.fetchall() if not row[0].startswith('sqlite_')]

        expected_tables = ['developers', 'projects', 'tasks']
        for table in expected_tables:
            self.assertIn(table, tables)

    def test_developers_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM developers")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)

        self.cursor.execute("SELECT * FROM developers LIMIT 1")
        developer = dict(self.cursor.fetchone())

        required_fields = ['id', 'full_name', 'position', 'hourly_rate']
        for field in required_fields:
            self.assertIn(field, developer)

    def test_projects_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM projects")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)

        self.cursor.execute("SELECT * FROM projects LIMIT 1")
        project = dict(self.cursor.fetchone())

        required_fields = ['id', 'name', 'client', 'deadline', 'budget']
        for field in required_fields:
            self.assertIn(field, project)

    def test_tasks_data(self):
        self.cursor.execute("SELECT COUNT(*) FROM tasks")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0)

        self.cursor.execute("SELECT * FROM tasks LIMIT 1")
        task = dict(self.cursor.fetchone())

        required_fields = ['id', 'project_id', 'developer_id', 'description', 'status', 'hours_worked']
        for field in required_fields:
            self.assertIn(field, task)

    def test_foreign_keys(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM tasks t
            LEFT JOIN projects p ON t.project_id = p.id
            WHERE p.id IS NULL
        """)
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

        self.cursor.execute("""
            SELECT COUNT(*) FROM tasks t
            LEFT JOIN developers d ON t.developer_id = d.id
            WHERE d.id IS NULL
        """)
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 0)

    def test_views(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='view'")
        views = [row[0] for row in self.cursor.fetchall()]

        expected_views = ['view_task_details', 'view_project_stats', 'view_developer_stats']
        for view in expected_views:
            self.assertIn(view, views)

        for view in expected_views:
            self.cursor.execute(f"SELECT COUNT(*) FROM {view}")
            count = self.cursor.fetchone()[0]
            self.assertGreater(count, 0)

    def test_task_details_view(self):
        self.cursor.execute("SELECT * FROM view_task_details LIMIT 1")
        task_details = dict(self.cursor.fetchone())

        required_fields = [
            'id', 'description', 'status', 'hours_worked',
            'project_id', 'project_name', 'project_deadline',
            'developer_id', 'developer_name', 'developer_position', 'hourly_rate'
        ]

        for field in required_fields:
            self.assertIn(field, task_details)

    def test_project_stats_view(self):
        self.cursor.execute("SELECT * FROM view_project_stats LIMIT 1")
        project_stats = dict(self.cursor.fetchone())

        required_fields = [
            'id', 'name', 'client', 'deadline', 'budget',
            'total_tasks', 'completed_tasks', 'completion_percentage',
            'total_hours', 'labor_cost'
        ]

        for field in required_fields:
            self.assertIn(field, project_stats)

    def test_developer_stats_view(self):
        self.cursor.execute("SELECT * FROM view_developer_stats LIMIT 1")
        developer_stats = dict(self.cursor.fetchone())

        required_fields = [
            'id', 'full_name', 'position', 'hourly_rate',
            'total_tasks', 'completed_tasks', 'total_hours', 'total_earnings'
        ]

        for field in required_fields:
            self.assertIn(field, developer_stats)

    def test_query_tasks_by_project(self):
        self.cursor.execute("SELECT id FROM projects LIMIT 1")
        project_id = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
        tasks = self.cursor.fetchall()

        self.assertGreater(len(tasks), 0)

    def test_query_tasks_by_developer(self):
        self.cursor.execute("SELECT id FROM developers LIMIT 1")
        developer_id = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT * FROM tasks WHERE developer_id = ?", (developer_id,))
        tasks = self.cursor.fetchall()

        self.assertGreater(len(tasks), 0)

    def test_query_tasks_by_status(self):
        self.cursor.execute("SELECT * FROM tasks WHERE status = 'в работе'")
        in_progress_tasks = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM tasks WHERE status = 'завершено'")
        completed_tasks = self.cursor.fetchall()

        self.assertGreater(len(in_progress_tasks) + len(completed_tasks), 0)

    def test_calculate_developer_salary(self):
        self.cursor.execute("SELECT id FROM developers LIMIT 1")
        developer_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT d.hourly_rate * SUM(t.hours_worked) as salary
            FROM developers d
            JOIN tasks t ON d.id = t.developer_id
            WHERE d.id = ?
            GROUP BY d.id
        """, (developer_id,))

        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertGreater(result['salary'], 0)

    def test_upsert_developer_trigger(self):
        """Test that the upsert_developer trigger prevents duplicates and updates existing records"""
        # Get an existing developer
        self.cursor.execute("SELECT * FROM developers LIMIT 1")
        existing_dev = dict(self.cursor.fetchone())

        # Try to insert a developer with the same name but different details
        new_hourly_rate = existing_dev['hourly_rate'] + 100
        new_position = 'QA' if existing_dev['position'] != 'QA' else 'backend'

        self.cursor.execute(
            "INSERT INTO developers (full_name, position, hourly_rate) VALUES (?, ?, ?)",
            (existing_dev['full_name'], new_position, new_hourly_rate)
        )
        self.__class__.conn.commit()

        # Check that the record was updated instead of duplicated
        self.cursor.execute("SELECT COUNT(*) FROM developers WHERE full_name = ?",
                            (existing_dev['full_name'],))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1, "Should have only one record with this name")

        # Check that the values were updated
        self.cursor.execute("SELECT * FROM developers WHERE full_name = ?",
                            (existing_dev['full_name'],))
        updated_dev = dict(self.cursor.fetchone())
        self.assertEqual(updated_dev['position'], new_position)
        self.assertEqual(updated_dev['hourly_rate'], new_hourly_rate)

    def test_upsert_project_trigger(self):
        """Test that the upsert_project trigger prevents duplicates and updates existing records"""
        # Get an existing project
        self.cursor.execute("SELECT * FROM projects LIMIT 1")
        existing_proj = dict(self.cursor.fetchone())

        # Try to insert a project with the same name and client but different details
        new_deadline = '2025-01-01'
        new_budget = existing_proj['budget'] + 100000

        self.cursor.execute(
            "INSERT INTO projects (name, client, deadline, budget) VALUES (?, ?, ?, ?)",
            (existing_proj['name'], existing_proj['client'], new_deadline, new_budget)
        )
        self.__class__.conn.commit()

        # Check that the record was updated instead of duplicated
        self.cursor.execute("SELECT COUNT(*) FROM projects WHERE name = ? AND client = ?",
                            (existing_proj['name'], existing_proj['client']))
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1, "Should have only one record with this name and client")

        # Check that the values were updated
        self.cursor.execute("SELECT * FROM projects WHERE name = ? AND client = ?",
                            (existing_proj['name'], existing_proj['client']))
        updated_proj = dict(self.cursor.fetchone())
        self.assertEqual(updated_proj['deadline'], new_deadline)
        self.assertEqual(updated_proj['budget'], new_budget)

    def test_upsert_task_trigger(self):
        self.cursor.execute("SELECT * FROM tasks LIMIT 1")
        existing_task = dict(self.cursor.fetchone())

        new_status = 'завершено' if existing_task['status'] == 'в работе' else 'в работе'
        new_hours = existing_task['hours_worked'] + 5

        self.cursor.execute(
            """INSERT INTO tasks 
               (project_id, developer_id, description, status, hours_worked) 
               VALUES (?, ?, ?, ?, ?)""",
            (existing_task['project_id'], existing_task['developer_id'],
             existing_task['description'], new_status, new_hours)
        )
        self.__class__.conn.commit()

        self.cursor.execute(
            """SELECT COUNT(*) FROM tasks 
               WHERE project_id = ? AND developer_id = ? AND description = ?""",
            (existing_task['project_id'], existing_task['developer_id'],
             existing_task['description'])
        )
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1, "Should have only one record with this project, developer and description")

        self.cursor.execute(
            """SELECT * FROM tasks 
               WHERE project_id = ? AND developer_id = ? AND description = ?""",
            (existing_task['project_id'], existing_task['developer_id'],
             existing_task['description'])
        )
        updated_task = dict(self.cursor.fetchone())
        self.assertEqual(updated_task['status'], new_status)
        self.assertEqual(updated_task['hours_worked'], new_hours)

    def test_insert_new_records_still_works(self):
        """Test that we can still insert completely new records"""
        new_dev_name = "Тестовый Разработчик"
        self.cursor.execute(
            "INSERT INTO developers (full_name, position, hourly_rate) VALUES (?, ?, ?)",
            (new_dev_name, 'backend', 2000)
        )
        self.__class__.conn.commit()

        self.cursor.execute("SELECT * FROM developers WHERE full_name = ?", (new_dev_name,))
        new_dev = self.cursor.fetchone()
        self.assertIsNotNone(new_dev)

        new_project_name = "Тестовый проект"
        new_client = "Тестовый клиент"
        self.cursor.execute(
            "INSERT INTO projects (name, client, deadline, budget) VALUES (?, ?, ?, ?)",
            (new_project_name, new_client, '2025-12-31', 300000)
        )
        self.__class__.conn.commit()

        self.cursor.execute("SELECT * FROM projects WHERE name = ? AND client = ?",
                            (new_project_name, new_client))
        new_project = self.cursor.fetchone()
        self.assertIsNotNone(new_project)

        new_task_desc = "Тестовая задача"
        self.cursor.execute(
            """INSERT INTO tasks 
               (project_id, developer_id, description, status, hours_worked) 
               VALUES (?, ?, ?, ?, ?)""",
            (new_project['id'], new_dev['id'], new_task_desc, 'в работе', 1)
        )
        self.__class__.conn.commit()

        self.cursor.execute(
            """SELECT * FROM tasks 
               WHERE project_id = ? AND developer_id = ? AND description = ?""",
            (new_project['id'], new_dev['id'], new_task_desc)
        )
        new_task = self.cursor.fetchone()
        self.assertIsNotNone(new_task)

    def test_project_progress(self):
        self.cursor.execute("SELECT id FROM projects LIMIT 1")
        project_id = self.cursor.fetchone()[0]

        self.cursor.execute("""
            SELECT 
                COUNT(*) as total_tasks,
                SUM(CASE WHEN status = 'завершено' THEN 1 ELSE 0 END) as completed_tasks,
                ROUND(SUM(CASE WHEN status = 'завершено' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as progress_percent
            FROM tasks
            WHERE project_id = ?
        """, (project_id,))

        result = dict(self.cursor.fetchone())
        self.assertGreater(result['total_tasks'], 0)
        self.assertGreaterEqual(result['progress_percent'], 0)
        self.assertLessEqual(result['progress_percent'], 100)


if __name__ == '__main__':
    unittest.main()