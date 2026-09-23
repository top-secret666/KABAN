from validation.base_validator import BaseValidator
from exceptions import ValidationException

class DeveloperValidator(BaseValidator):
    """
    Валидатор для данных разработчика
    """
    @classmethod
    def validate(cls, data):
        """
        Валидирует данные разработчика
        """
        if not isinstance(data, dict):
            raise ValidationException("Данные должны быть словарем")
        
        # Проверка обязательных полей
        cls.validate_not_empty(data.get('full_name'), 'full_name')
        cls.validate_not_empty(data.get('position'), 'position')
        
        # Проверка hourly_rate
        if 'hourly_rate' in data:
            data['hourly_rate'] = cls.validate_positive_number(data['hourly_rate'], 'hourly_rate')
        
        # Проверка допустимых значений для position
        valid_positions = ['frontend', 'backend', 'fullstack', 'designer', 'tester', 'manager']
        if data.get('position') and data['position'] not in valid_positions:
            raise ValidationException(
                f"Недопустимое значение. Допустимые значения: {', '.join(valid_positions)}", 
                'position'
            )
        
        return data
