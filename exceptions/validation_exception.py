from exceptions.base_exception import KabanException

class ValidationException(KabanException):
    """
    Исключение, возникающее при ошибках валидации данных
    """
    def __init__(self, message="Ошибка валидации данных", field=None):
        self.field = field
        if field:
            message = f"Ошибка валидации поля '{field}': {message}"
        super().__init__(message)
