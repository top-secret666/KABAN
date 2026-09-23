from validation.base_validator import BaseValidator
from exceptions import ValidationException
from datetime import datetime, timedelta

class ProjectValidator(BaseValidator):
    """
    Валидатор для данных проекта
    """
    @classmethod
    def validate(cls, data):
        """
        Валидирует данные проекта
        """
        if not isinstance(data, dict):
            raise ValidationException("Данные должны быть словарем")
        
        # Проверка обязательных полей
        cls.validate_not_empty(data.get('name'), 'name')
        cls.validate_not_empty(data.get('client'), 'client')
        
        # Проверка deadline
        if 'deadline' in data and data['deadline']:
            data['deadline'] = cls.validate_date_format(data['deadline'], 'deadline')
            
            # Получаем текущую дату и вычисляем границы
            today = datetime.now().date()
            min_deadline = today - timedelta(days=365*10)  # 10 лет назад
            max_deadline = today + timedelta(days=365*20)  # 20 лет вперед
            deadline_date = datetime.strptime(data['deadline'], '%Y-%m-%d').date()

            # Проверка, что дедлайн не более 10 лет в прошлом
            if deadline_date < min_deadline:
                raise ValidationException(f"Дедлайн не может быть более чем 10 лет в прошлом (не ранее {min_deadline.strftime('%Y-%m-%d')})", 'deadline')

            # Проверка, что дедлайн не более 20 лет в будущем
            if deadline_date > max_deadline:
                raise ValidationException(f"Дедлайн не может быть более чем через 20 лет от текущей даты (не позднее {max_deadline.strftime('%Y-%m-%d')})", 'deadline')

        # Проверка budget
        if 'budget' in data:
            data['budget'] = cls.validate_positive_number(data['budget'], 'budget')
        
        return data
