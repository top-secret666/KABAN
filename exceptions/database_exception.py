from exceptions.base_exception import KabanException

class DatabaseException(KabanException):
    """
    Исключение, возникающее при ошибках работы с базой данных
    """
    def __init__(self, message="Ошибка при работе с базой данных", sql_error=None):
        self.sql_error = sql_error
        if sql_error:
            message = f"{message}: {str(sql_error)}"
        super().__init__(message)
