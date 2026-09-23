import sqlite3
import os
import sys


def init_database(db_path='database/kabanmanagement_it-projects.sqlite', sql_path='database/kaban.sql'):
    try:
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        if not os.path.exists(sql_path):
            print(f"Ошибка: SQL-файл '{sql_path}' не найден")
            return False

        with open(sql_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()

        conn = sqlite3.connect(db_path)
        conn.executescript(sql_script)
        conn.close()

        print(f"База данных успешно инициализирована: {db_path}")
        return True

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        return False


def test_connection(db_path='database/kabanmanagement_it-projects.sqlite'):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Таблицы в базе данных:")
        for table in tables:
            print(f"- {table[0]}")

        for table_name in ['developers', 'projects', 'tasks', 'users', 'notifications', 'sessions']:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"Количество записей в таблице {table_name}: {count}")

        conn.close()
        return True

    except Exception as e:
        print(f"Ошибка при тестировании подключения к базе данных: {e}")
        return False


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(script_dir, '..', 'database')
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)
    db_path = os.path.join(db_folder, 'kabanmanagement_it-projects.sqlite')
    sql_path = os.path.join(script_dir, 'kaban.sql')

    if init_database(db_path, sql_path):
        test_connection(db_path)
    else:
        sys.exit(1)