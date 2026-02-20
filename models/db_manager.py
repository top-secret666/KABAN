import sqlite3
import os


class DBManager:
    _instance = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.db_path = db_path or os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kaban.db')
            cls._instance.conn = None
            cls._instance.cursor = None
        return cls._instance


    def begin_transaction(self):
        """
        Начинает новую транзакцию
        """
        try:
            self.connect()
            self.conn.execute("BEGIN TRANSACTION")
            return True
        except Exception as e:
            print(f"Ошибка при начале транзакции: {e}")
            return False

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute(self, query, params=None):
        self.connect()
        if params:
            return self.cursor.execute(query, params)
        return self.cursor.execute(query)

    def execute_many(self, query, params_list):
        self.connect()
        return self.cursor.executemany(query, params_list)

    def fetch_one(self):
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def fetch_all(self):
        """
         Получает все строки результата запроса

         Returns:
             list: Список словарей с данными
         """
        if self.cursor:
            columns = [column[0] for column in self.cursor.description]
            print(f"Столбцы в результате запроса: {columns}")

            result = []
            for row in self.cursor.fetchall():
                row_dict = dict(zip(columns, row))
                print(f"Строка из базы данных: {row_dict}")
                result.append(row_dict)

            return result
        return []

    def commit(self):
        """
        Фиксирует изменения в базе данных
        """
        try:
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при фиксации изменений: {e}")
            return False

    @staticmethod
    def check_projects_status():
        db_manager = DBManager()
        db_manager.connect()
        db_manager.execute("SELECT id, name, status FROM projects")
        results = db_manager.fetch_all()
        print("Результаты прямого запроса:")
        for result in results:
            print(f"ID: {result.get('id')}, Название: {result.get('name')}, Статус: {result.get('status')}")

    @staticmethod
    def check_table_structure():
        db_manager = DBManager()
        db_manager.connect()
        db_manager.execute("PRAGMA table_info(projects)")
        columns = db_manager.fetch_all()
        print("Структура таблицы projects:")
        for column in columns:
            print(f"Имя: {column.get('name')}, Тип: {column.get('type')}")

    def rollback(self):
        """
        Откатывает изменения в базе данных
        """
        try:
            self.conn.rollback()
            return True
        except Exception as e:
            print(f"Ошибка при откате изменений: {e}")
            return False

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def get_last_row_id(self):
        return self.cursor.lastrowid

    def table_exists(self, table_name):
        self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return self.fetch_one() is not None

    def create_tables_if_not_exist(self):
        try:
            tables = ['developers', 'projects', 'tasks']
            for table in tables:
                if not self.table_exists(table):
                    script_dir = os.path.dirname(os.path.dirname(__file__))
                    sql_path = os.path.join(script_dir, 'database', 'kaban.sql')

                    if not os.path.exists(sql_path):
                        return False

                    with open(sql_path, 'r', encoding='utf-8') as sql_file:
                        sql_script = sql_file.read()

                    self.conn.executescript(sql_script)
                    self.commit()
                    return True

            return True



        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            return False