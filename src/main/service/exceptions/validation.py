class ValidationException(Exception):
    def __init__(self, message="Ошибка валидации данных", field=None):
        self.field = field
        if field:
            message = f"Ошибка валидации поля '{field}': {message}"
        super().__init__(message)
