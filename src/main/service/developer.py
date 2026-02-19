from src.main.models import Developer
from .utils import DeveloperValidator
from .exceptions import BusinessException, ValidationException, DatabaseException


class DeveloperService:
    def execute_query(self, query, params=None):
        db_manager = Developer().db_manager
        db_manager.connect()
        if params:
            return db_manager.execute(query, params)
        return db_manager.execute(query)

    def get_all_developers(self):
        try:
            query = "SELECT id, full_name, position, hourly_rate FROM developers"
            cursor = self.execute_query(query)

            developers = []
            for row in cursor.fetchall():
                developer = Developer(
                    id=row[0],
                    full_name=row[1],
                    position=row[2],
                    hourly_rate=row[3]
                )
                developers.append(developer)

            return developers
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка разработчиков: {str(e)}")

    def get_developer_by_id(self, developer_id):
        try:
            return Developer.get_by_id(developer_id)
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении разработчика: {str(e)}")

    def create_developer(self, data):
        try:
            validated_data = DeveloperValidator.validate(data)

            query = "SELECT id FROM developers WHERE full_name = ?"
            cursor = self.execute_query(query, [validated_data['full_name']])
            existing_developer = cursor.fetchone()

            if existing_developer:
                developer_id = existing_developer[0]
                developer = Developer.get_by_id(developer_id)

                if 'position' in validated_data:
                    developer.position = validated_data['position']
                if 'hourly_rate' in validated_data:
                    developer.hourly_rate = validated_data['hourly_rate']

                success, error = developer.save()
                if not success:
                    raise BusinessException(f"Не удалось обновить существующего разработчика: {error}")

                return developer
            else:
                developer = Developer(
                    full_name=validated_data['full_name'],
                    position=validated_data['position'],
                    hourly_rate=validated_data.get('hourly_rate', 0)
                )

                success, error = developer.save()
                if not success:
                    raise BusinessException(f"Не удалось создать разработчика: {error}")

                return developer
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при создании/обновлении разработчика: {str(e)}")

    def update_developer(self, developer_id, data):
        """
        Обновляет данные разработчика
        """
        try:
            # Получение разработчика
            developer = self.get_developer_by_id(developer_id)
            if not developer:
                raise BusinessException(f"Разр��ботчик с ID {developer_id} не найден")

            # Валидация данных
            validated_data = DeveloperValidator.validate(data)

            # Обновление полей
            developer.full_name = validated_data['full_name']
            developer.position = validated_data['position']
            developer.hourly_rate = validated_data.get('hourly_rate', developer.hourly_rate)

            # Сохранение изменений
            success, error = developer.save()
            if not success:
                raise BusinessException(f"Не удалось обновить разработчика: {error}")

            return developer
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении разработчика: {str(e)}")

    def delete_developer(self, developer_id):
        try:
            developer = self.get_developer_by_id(developer_id)
            if not developer:
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")

            tasks = developer.get_tasks()
            if tasks:
                raise BusinessException(
                    f"Невозможно удалить разработчика, так как у него есть {len(tasks)} назначенных задач"
                )

            success, error = developer.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить разработчика: {error}")

            return True
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении разработчика: {str(e)}")

    def search_developers(self, search_term=None, position=None):
        try:
            query = "SELECT id, full_name, position, hourly_rate FROM developers WHERE 1=1"
            params = []

            if search_term:
                query += " AND full_name LIKE ?"
                params.append(f"%{search_term}%")

            if position:
                query += " AND position = ?"
                params.append(position)

            cursor = self.execute_query(query, params)

            developers = []
            for row in cursor.fetchall():
                developer = Developer(
                    id=row[0],
                    full_name=row[1],
                    position=row[2],
                    hourly_rate=row[3]
                )
                developers.append(developer)

            return developers
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при поиске разработчиков: {str(e)}")

    def calculate_developer_salary(self, developer_id, start_date=None, end_date=None):
        try:
            developer = self.get_developer_by_id(developer_id)
            if not developer:
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")

            query = """
                SELECT SUM(hours_worked) 
                FROM tasks 
                WHERE developer_id = ?
            """
            params = [developer_id]

            if start_date:
                query += " AND date(created_at) >= date(?)"
                params.append(start_date)

            if end_date:
                query += " AND date(created_at) <= date(?)"
                params.append(end_date)

            cursor = self.execute_query(query, params)
            total_hours = cursor.fetchone()[0] or 0

            salary = total_hours * developer.hourly_rate

            return {
                'developer': developer,
                'total_hours': total_hours,
                'hourly_rate': developer.hourly_rate,
                'salary': salary,
                'start_date': start_date,
                'end_date': end_date
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при расчете зарплаты: {str(e)}")
