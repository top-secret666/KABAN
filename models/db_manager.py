import sqlite3
import os

from paths import DB_PATH


class DBManager:
    _instance = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance.db_path = db_path or DB_PATH
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
        except Exception:
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
            return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return []

    def commit(self):
        """
        Фиксирует изменения в базе данных
        """
        try:
            self.conn.commit()
            return True
        except Exception:
            return False

    def rollback(self):
        if self.conn:
            try:
                self.conn.rollback()
            except Exception:
                return False
            return True
        return False

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



        except Exception:
            return False