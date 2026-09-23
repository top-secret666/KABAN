from controllers.base_controller import BaseController
from services import DeveloperService


class DeveloperController(BaseController):
    """Контроллер для управления разработчиками."""

    def __init__(self, service=None):
        super().__init__(service or DeveloperService())

    def get_all_developers(self):
        return self.execute_service_method('get_all_developers')

    def get_developer_by_id(self, developer_id):
        return self.execute_service_method('get_developer_by_id', developer_id)

    def get_developer_by_user_id(self, user_id):
        try:
            from models import DBManager
            from models.developer import Developer

            db_manager = DBManager()
            db_manager.connect()

            query = """
                SELECT d.id, d.full_name, d.position, d.hourly_rate
                FROM developers d
                WHERE d.user_id = ?
            """
            db_manager.execute(query, (user_id,))
            result = db_manager.fetch_one()

            if result:
                developer = Developer(
                    id=result['id'],
                    full_name=result['full_name'],
                    position=result['position'],
                    hourly_rate=result['hourly_rate'],
                )
                return {'success': True, 'data': developer, 'error_message': None}

            user_query = "SELECT full_name FROM users WHERE id = ?"
            db_manager.execute(user_query, (user_id,))
            user_result = db_manager.fetch_one()

            if not user_result:
                return {
                    'success': False,
                    'data': None,
                    'error_message': f"Пользователь с ID {user_id} не найден",
                }

            name_query = """
                SELECT id, full_name, position, hourly_rate
                FROM developers
                WHERE full_name = ?
            """
            db_manager.execute(name_query, (user_result['full_name'],))
            name_result = db_manager.fetch_one()

            if name_result:
                developer = Developer(
                    id=name_result['id'],
                    full_name=name_result['full_name'],
                    position=name_result['position'],
                    hourly_rate=name_result['hourly_rate'],
                )
                db_manager.execute(
                    "UPDATE developers SET user_id = ? WHERE id = ?",
                    (user_id, developer.id),
                )
                db_manager.commit()
                return {'success': True, 'data': developer, 'error_message': None}

            return {
                'success': False,
                'data': None,
                'error_message': f"Разработчик для пользователя с ID {user_id} не найден",
            }

        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error_message': f"Ошибка при получении разработчика по user_id: {str(e)}",
            }

    def create_developer(self, data):
        return self.execute_service_method('create_developer', data)

    def update_developer(self, developer_id, data):
        return self.execute_service_method('update_developer', developer_id, data)

    def delete_developer(self, developer_id):
        return self.execute_service_method('delete_developer', developer_id)

    def search_developers(self, search_term=None, position=None):
        return self.execute_service_method('search_developers', search_term, position)

    def calculate_developer_salary(self, developer_id, start_date=None, end_date=None):
        return self.execute_service_method(
            'calculate_developer_salary', developer_id, start_date, end_date
        )

    def get_developer_positions(self):
        return {
            'success': True,
            'data': ['frontend', 'backend', 'fullstack', 'designer', 'tester', 'manager'],
        }
