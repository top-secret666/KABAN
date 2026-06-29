from validation.base_validator import BaseValidator
from exceptions import ValidationException

class TaskValidator(BaseValidator):
    """
    Валидатор для данных задачи
    """
    @classmethod
    def validate(cls, data):
        """
        Валидирует данные задачи
        """
        if not isinstance(data, dict):
            raise ValidationException("Данные должны быть словарем")
        
        # Проверка обязательных полей
        cls.validate_not_empty(data.get('description'), 'description')
        
        # Проверка project_id
        if 'project_id' in data:
            data['project_id'] = cls.validate_positive_number(data['project_id'], 'project_id')
        else:
            raise ValidationException("Проект обязателен", 'project_id')
        
        # Проверка developer_id (может быть None, если задача не назначена)
        if 'developer_id' in data and data['developer_id'] is not None:
            data['developer_id'] = cls.validate_positive_number(data['developer_id'], 'developer_id')
        
        # Проверка hours_worked
        if 'hours_worked' in data:
            data['hours_worked'] = cls.validate_positive_number(data['hours_worked'], 'hours_worked')
        
        # Проверка status
        valid_statuses = ['новая', 'в работе', 'на проверке', 'завершено']
        if 'status' in data:
            cls.validate_not_empty(data['status'], 'status')
            if data['status'] not in valid_statuses:
                raise ValidationException(
                    f"Недопустимый статус. Допустимые значения: {', '.join(valid_statuses)}", 
                    'status'
                )
        
        return data

