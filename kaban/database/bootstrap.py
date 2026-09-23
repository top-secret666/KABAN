"""Инициализация базы данных при запуске."""
import os

from paths import DB_PATH, SQL_PATH
from models import DBManager


def ensure_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db_manager = DBManager(DB_PATH)
    db_manager.connect()

    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        with open(SQL_PATH, 'r', encoding='utf-8') as sql_file:
            db_manager.conn.executescript(sql_file.read())
        db_manager.commit()

    return db_manager
