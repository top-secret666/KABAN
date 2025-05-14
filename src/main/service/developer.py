from src.main.models import Developer
from utils import DeveloperValidator
from exceptions import BusinessException, ValidationException, DatabaseException


class DeveloperService:

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
            raise BusinessException(f"Ошибка при создании разработчика: {str(e)}")

    def update_developer(self, developer_id, data):
        try:
            developer = self.get_developer_by_id(developer_id)
            if not developer:
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")

            validated_data = DeveloperValidator.validate(data)

            developer.full_name = validated_data['full_name']
            developer.position = validated_data['position']
            developer.hourly_rate = validated_data.get('hourly_rate', developer.hourly_rate)

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
