from services.base_service import BaseService
from models import Developer
from validation import DeveloperValidator
from exceptions import BusinessException, ValidationException, DatabaseException

class DeveloperService(BaseService):
    """
    Сервис для работы с разработчиками
    """
    def get_all_developers(self):
        """
        Получает список всех разработчиков
        """
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
        """
        Получает разработчика по ID
        """
        query = "SELECT id, full_name, position, hourly_rate FROM developers WHERE id = ?"
        result = self.db_manager.execute(query, (developer_id,)).fetchone()

        if not result:
            raise BusinessException(f"Разработчик с ID {developer_id} не найден")

        return Developer(*result)

    def create_developer(self, data):
        """
        Создает нового разработчика или обновляет существующего, если найден дубликат
        """
        try:
            # Валидация данных
            validated_data = DeveloperValidator.validate(data)
            
            # Проверка на дубликаты по полному имени
            query = "SELECT id FROM developers WHERE full_name = ?"
            cursor = self.execute_query(query, [validated_data['full_name']])
            existing_developer = cursor.fetchone()
            
            if existing_developer:
                # Если разработчик с таким именем уже существует, обновляем его
                developer_id = existing_developer[0]
                developer = Developer.get_by_id(developer_id)
                
                # Обновляем только те поля, которые предоставлены
                if 'position' in validated_data:
                    developer.position = validated_data['position']
                if 'hourly_rate' in validated_data:
                    developer.hourly_rate = validated_data['hourly_rate']
                
                # Сохраняем изменения
                success, error = developer.save()
                if not success:
                    raise BusinessException(f"Не удалось обновить существующего разработчика: {error}")
                
                return developer
            else:
                # Создание нового объекта разработчика
                developer = Developer(
                    full_name=validated_data['full_name'],
                    position=validated_data['position'],
                    hourly_rate=validated_data.get('hourly_rate', 0)
                )
                
                # Сохранение в базу данных
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
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")
            
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
        """
        Удаляет разработчика по ID
        """
        try:
            developer = self.get_developer_by_id(developer_id)
            # Проверяем, что разработчик существует
            if not developer:
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")

            # Удаляем разработчика из базы данных
            query = "DELETE FROM developers WHERE id = ?"
            self.db_manager.execute(query, (developer_id,))
            self.db_manager.commit()

            return True
        except Exception as e:
            self.db_manager.rollback()
            raise BusinessException(f"Ошибка при удалении разработчика: {str(e)}")

            # Удаление разработчика
            success, error = developer.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить разработчика: {error}")
            
            return True
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении разработчика: {str(e)}")
    
    def search_developers(self, search_term=None, position=None):
        """
        Поиск разработчиков по имени и/или должности
        """
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
        """
        Расчет зарплаты разработчика за период
        """
        try:
            # Получение разработчика
            developer = self.get_developer_by_id(developer_id)
            if not developer:
                raise BusinessException(f"Разработчик с ID {developer_id} не найден")
            
            # Формирование запроса для получения задач за период
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
            
            # Расчет зарплаты
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
