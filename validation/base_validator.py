from exceptions import ValidationException

class BaseValidator:
    """
    Базовый класс для валидаторов
    """
    @staticmethod
    def validate_not_empty(value, field_name):
        """
        Проверяет, что значение не пустое
        """
        if value is None or (isinstance(value, str) and value.strip() == ''):
            raise ValidationException("Поле не может быть пустым", field_name)
        return value
    
    @staticmethod
    def validate_positive_number(value, field_name):
        """
        Проверяет, что значение является положительным числом
        """
        try:
            num_value = float(value)
            if num_value < 0:
                raise ValidationException("Значение должно быть положительным числом", field_name)
            return num_value
        except (ValueError, TypeError):
            raise ValidationException("Значение должно быть числом", field_name)
    
    @staticmethod
    def validate_date_format(value, field_name):
        """
        Проверяет, что значение соответствует формату даты YYYY-MM-DD
        """
        import re
        if not value:
            return None
        
        if not isinstance(value, str):
            raise ValidationException("Дата должна быть строкой", field_name)
        
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(pattern, value):
            raise ValidationException("Дата должна быть в формате YYYY-MM-DD", field_name)
        
        try:
            from datetime import datetime
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            raise ValidationException("Некорректная дата", field_name)
