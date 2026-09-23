from exceptions import ValidationException, DatabaseException, BusinessException

class BaseController:
    """
    Базовый класс для всех контроллеров
    """
    def __init__(self, service=None):
        """
        Инициализирует контроллер с соответствующим сервисом
        """
        self.service = service
    
    def handle_exception(self, exception):
        """
        Обрабатывает исключения и возвращает информацию для UI
        """
        error_message = str(exception)
        error_type = "Ошибка"
        
        if isinstance(exception, ValidationException):
            error_type = "Ошибка валидации"
        elif isinstance(exception, DatabaseException):
            error_type = "Ошибка базы данных"
        elif isinstance(exception, BusinessException):
            error_type = "Ошибка бизнес-логики"
        
        return {
            'success': False,
            'error_type': error_type,
            'error_message': error_message
        }
    
    def execute_service_method(self, method_name, *args, **kwargs):
        """
        Выполняет метод сервиса и обрабатывает исключения
        """
        try:
            method = getattr(self.service, method_name)
            result = method(*args, **kwargs)
            return {
                'success': True,
                'data': result
            }
        except Exception as e:
            return self.handle_exception(e)
