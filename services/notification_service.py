from services.base_service import BaseService
from models.notification import Notification
from exceptions import BusinessException, ValidationException, DatabaseException
from datetime import datetime, timedelta

class NotificationService(BaseService):
    """
    Сервис для работы с уведомлениями
    """
    def get_all_notifications(self, limit=None, offset=None, only_unread=False):
        """
        Получает список всех уведомлений
        
        Args:
            limit: Ограничение количества результатов
            offset: Смещение результатов
            only_unread: Только непрочитанные уведомления
        
        Returns:
            list: Список уведомлений
        """
        try:
            return Notification.get_all(limit, offset, only_unread, self.db_manager)
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка уведомлений: {str(e)}")
    
    def get_notification_by_id(self, notification_id):
        """
        Получает уведомление по ID
        
        Args:
            notification_id: ID уведомления
        
        Returns:
            Notification: Объект уведомления
        """
        try:
            notification = Notification.get_by_id(notification_id, self.db_manager)
            if not notification:
                raise BusinessException(f"Уведомление с ID {notification_id} не найдено")
            return notification
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении уведомления: {str(e)}")

    def create_notification(self, title, message, type='info', related_id=None, related_type=None, user_id=None):
        """
        Создает новое уведомление

        Args:
            title: Заголовок уведомления
            message: Текст уведомления
            type: Тип уведомления (info, warning, error)
            related_id: ID связанного объекта
            related_type: Тип связанного объекта
            user_id: ID пользователя, которому адресовано уведомление

        Returns:
            Notification: Созданное уведомление
        """
        try:
            print(f"Создание уведомления: {title}")

            # Если user_id не указан, отправляем уведомление всем пользователям (NULL)
            notification = Notification(
                title=title,
                message=message,
                type=type,
                related_id=related_id,
                related_type=related_type,
                is_read=False,
                user_id=user_id,
                db_manager=self.db_manager
            )

            success, error = notification.save()
            if not success:
                print(f"Ошибка при сохранении уведомления: {error}")
                raise BusinessException(f"Не удалось создать уведомление: {error}")

            print(f"Уведомление успешно создано с ID: {notification.id}")
            return notification
        except Exception as e:
            print(f"Исключение при создании уведомления: {str(e)}")
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при создании уведомления: {str(e)}")

    def mark_as_read(self, notification_id):
        """
        Отмечает уведомление как прочитанное
        
        Args:
            notification_id: ID уведомления
        
        Returns:
            bool: Результат операции
        """
        try:
            notification = self.get_notification_by_id(notification_id)
            success, error = notification.mark_as_read()
            if not success:
                raise BusinessException(f"Не удалось отметить уведомление как прочитанное: {error}")
            return True
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении уведомления: {str(e)}")
    
    def mark_all_as_read(self):
        """
        Отмечает все уведомления как прочитанные
        
        Returns:
            int: Количество обновленных уведомлений
        """
        try:
            query = "UPDATE notifications SET is_read = 1 WHERE is_read = 0"
            cursor = self.execute_query(query)
            self.commit()
            return cursor.rowcount
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при обновлении уведомлений: {str(e)}")
    
    def delete_notification(self, notification_id):
        """
        Удаляет уведомление
        
        Args:
            notification_id: ID уведомления
        
        Returns:
            bool: Результат операции
        """
        try:
            notification = self.get_notification_by_id(notification_id)
            success, error = notification.delete()
            if not success:
                raise BusinessException(f"Не удалось удалить уведомление: {error}")
            return True
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении уведомления: {str(e)}")
    
    def delete_all_read_notifications(self):
        """
        Удаляет все прочитанные уведомления
        
        Returns:
            int: Количество удаленных уведомлений
        """
        try:
            query = "DELETE FROM notifications WHERE is_read = 1"
            cursor = self.execute_query(query)
            self.commit()
            return cursor.rowcount
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при удалении уведомлений: {str(e)}")

    def check_overdue_projects(self):
        """
        Проверяет просроченные проекты и создает уведомления

        Returns:
            int: Количество созданных уведомлений
        """
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            print(f"Проверка просроченных проектов. Текущая дата: {today}")

            # Упрощенный запрос без проверки существующих уведомлений
            query = """
                SELECT id, name, deadline
                FROM projects
                WHERE deadline < ? AND status != 'завершено'
            """
            cursor = self.execute_query(query, [today])

            projects = cursor.fetchall()
            print(f"Найдено просроченных проектов: {len(projects)}")

            count = 0
            for row in projects:
                project_id = row[0]
                project_name = row[1]
                deadline = row[2]

                print(f"Создание уведомления для просроченного проекта: {project_name} (ID: {project_id})")

                # Создаем уведомление о просроченном проекте
                notification = self.create_notification(
                    title="Просрочен дедлайн проекта",
                    message=f"Проект '{project_name}' просрочен. Дедлайн был {deadline}.",
                    type="warning",
                    related_id=project_id,
                    related_type="project_overdue"
                )

                if notification:
                    count += 1
                    print(f"Уведомление создано успешно: {notification.id}")
                else:
                    print("Ошибка при создании уведомления")

            return count
        except Exception as e:
            import traceback
            print(f"Ошибка при проверке просроченных проектов: {str(e)}")
            print(traceback.format_exc())
            return 0

    def check_upcoming_deadlines(self, days=3):
        """
        Проверяет приближающиеся дедлайны и создает уведомления
        
        Args:
            days: Количество дней до дедлайна для создания уведомления
        
        Returns:
            int: Количество созданных уведомлений
        """
        try:
            today = datetime.now().date()
            future_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Получаем проекты, у которых дедлайн через указанное количество дней
            query = """
                SELECT id, name, deadline
                FROM projects
                WHERE date(deadline) = ? AND deadline IS NOT NULL
                AND id NOT IN (
                    SELECT related_id FROM notifications 
                    WHERE related_type = 'project_upcoming' AND related_id IS NOT NULL
                )
            """
            cursor = self.execute_query(query, [future_date])
            
            count = 0
            for row in cursor.fetchall():
                project_id = row[0]
                project_name = row[1]
                deadline = row[2]
                
                # Создаем уведомление о приближающемся дедлайне
                self.create_notification(
                    title="Приближается дедлайн проекта",
                    message=f"До дедлайна проекта '{project_name}' осталось {days} дней. Дедлайн: {deadline}.",
                    type="info",
                    related_id=project_id,
                    related_type="project_upcoming"
                )
                count += 1
            
            return count
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при проверке приближающихся дедлайнов: {str(e)}")
    
    def check_inactive_tasks(self, days=7):
        """
        Проверяет неактивные задачи и создает уведомления
        
        Args:
            days: Количество дней неактивности для создания уведомления
        
        Returns:
            int: Количество созданных уведомлений
        """
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # Получаем задачи, которые не обновлялись более указанного количества дней и не завершены
            query = """
                SELECT t.id, t.description, p.name as project_name, d.full_name as developer_name
                FROM tasks t
                JOIN projects p ON t.project_id = p.id
                LEFT JOIN developers d ON t.developer_id = d.id
                WHERE t.status != 'завершено' AND date(t.updated_at) <= ?
                AND t.id NOT IN (
                    SELECT related_id FROM notifications 
                    WHERE related_type = 'task_inactive' AND related_id IS NOT NULL
                )
            """
            cursor = self.execute_query(query, [cutoff_date])
            
            count = 0
            for row in cursor.fetchall():
                task_id = row[0]
                task_description = row[1]
                project_name = row[2]
                developer_name = row[3] or "Не назначен"
                
                # Создаем уведомление о неактивной задаче
                self.create_notification(
                    title="Неактивная задача",
                    message=f"Задача '{task_description}' в проекте '{project_name}' (разработчик: {developer_name}) не обновлялась более {days} дней.",
                    type="warning",
                    related_id=task_id,
                    related_type="task_inactive"
                )
                count += 1
            
            return count
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при проверке неактивных задач: {str(e)}")
    
    def check_budget_warnings(self, threshold=0.8):
        """
        Проверяет проекты с превышением бюджета и создает уведомления
        
        Args:
            threshold: Порог использования бюджета для создания уведомления (0.8 = 80%)
        
        Returns:
            int: Количество созданных уведомлений
        """
        try:
            # Получаем проекты, у которых использовано более указанного процента бюджета
            query = """
                SELECT p.id, p.name, p.budget, SUM(t.hours_worked * d.hourly_rate) as cost
                FROM projects p
                JOIN tasks t ON p.id = t.project_id
                JOIN developers d ON t.developer_id = d.id
                WHERE p.budget > 0
                GROUP BY p.id
                HAVING cost >= p.budget * ?
                AND p.id NOT IN (
                    SELECT related_id FROM notifications 
                    WHERE related_type = 'budget_warning' AND related_id IS NOT NULL
                )
            """
            cursor = self.execute_query(query, [threshold])
            
            count = 0
            for row in cursor.fetchall():
                project_id = row[0]
                project_name = row[1]
                budget = row[2]
                cost = row[3]
                percent = (cost / budget) * 100
                
                # Создаем уведомление о превышении бюджета
                self.create_notification(
                    title="Предупреждение о бюджете",
                    message=f"Проект '{project_name}' использовал {percent:.1f}% бюджета ({cost:.2f} из {budget:.2f}).",
                    type="warning" if cost < budget else "error",
                    related_id=project_id,
                    related_type="budget_warning"
                )
                count += 1
            
            return count
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при проверке бюджета проектов: {str(e)}")
    
    def run_all_checks(self):
        """
        Запускает все проверки и создает уведомления
        
        Returns:
            dict: Количество созданных уведомлений по каждой проверке
        """
        try:
            overdue = self.check_overdue_projects()
            upcoming = self.check_upcoming_deadlines()
            inactive = self.check_inactive_tasks()
            budget = self.check_budget_warnings()
            
            return {
                'overdue_projects': overdue,
                'upcoming_deadlines': upcoming,
                'inactive_tasks': inactive,
                'budget_warnings': budget,
                'total': overdue + upcoming + inactive + budget
            }
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при выполнении проверок: {str(e)}")
