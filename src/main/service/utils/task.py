from src.main.service.exceptions import ValidationException


class TaskValidator:
    @classmethod
    def validate(cls, data):
        if not isinstance(data, dict):
            raise ValidationException("Данные должны быть словарем")

        cls.validate_not_empty(data.get('description'), 'description')

        if 'project_id' in data:
            data['project_id'] = cls.validate_positive_number(data['project_id'], 'project_id')
        else:
            raise ValidationException("Проект обязателен", 'project_id')

        if 'developer_id' in data and data['developer_id'] is not None:
            data['developer_id'] = cls.validate_positive_number(data['developer_id'], 'developer_id')

        if 'hours_worked' in data:
            data['hours_worked'] = cls.validate_positive_number(data['hours_worked'], 'hours_worked')

        valid_statuses = ['новая', 'в работе', 'на проверке', 'завершено']
        if 'status' in data:
            cls.validate_not_empty(data['status'], 'status')
            if data['status'] not in valid_statuses:
                raise ValidationException(
                    f"Недопустимый статус. Допустимые значения: {', '.join(valid_statuses)}",
                    'status'
                )

        return data
