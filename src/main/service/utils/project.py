from src.main.service.exceptions import ValidationException
from datetime import datetime


class ProjectValidator:
    @classmethod
    def validate(cls, data):

        if not isinstance(data, dict):
            raise ValidationException("Данные должны быть словарем")

        cls.validate_not_empty(data.get('name'), 'name')
        cls.validate_not_empty(data.get('client'), 'client')

        if 'deadline' in data and data['deadline']:
            data['deadline'] = cls.validate_date_format(data['deadline'], 'deadline')

            today = datetime.now().date()
            deadline_date = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            if deadline_date < today:
                raise ValidationException("Дедлайн не может быть в прошлом", 'deadline')

        if 'budget' in data:
            data['budget'] = cls.validate_positive_number(data['budget'], 'budget')

        return data
