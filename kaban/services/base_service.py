from models import DBManager
from exceptions import DatabaseException, ValidationException, BusinessException
import sqlite3

class BaseService:
    """
    Базовый класс для всех сервисов
    """
    def __init__(self, db_manager=None):
        """
        Инициализирует сервис с менеджером базы данных
        """
        self.db_manager = db_manager or DBManager()
    
    def execute_query(self, query, params=None):
        """
        Выполняет SQL-запрос и обрабатывает исключения
        """
        try:
            cursor = self.db_manager.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            raise DatabaseException(f"Ошибка при выполнении запроса: {query}", e)
    
    def commit(self):
        """
        Фиксирует изменения в базе данных
        """
        try:
            self.db_manager.commit()
        except sqlite3.Error as e:
            raise DatabaseException("Ошибка при фиксации изменений", e)
    
    def rollback(self):
        """
        Откатывает изменения в базе данных
        """
        try:
            self.db_manager.rollback()
        except sqlite3.Error as e:
            raise DatabaseException("Ошибка при откате изменений", e)
