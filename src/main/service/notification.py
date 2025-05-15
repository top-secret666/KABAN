from src.main.models.notification import Notification
from exceptions import BusinessException, ValidationException, DatabaseException
from datetime import datetime, timedelta


class NotificationService:
    def get_all_notifications(self, limit=None, offset=None, only_unread=False):
        try:
            return Notification.get_all(limit, offset, only_unread, self.db_manager)
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении списка уведомлений: {str(e)}")

    def get_notification_by_id(self, notification_id):
        try:
            notification = Notification.get_by_id(notification_id, self.db_manager)
            if not notification:
                raise BusinessException(f"Уведомление с ID {notification_id} не найдено")
            return notification
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при получении уведомления: {str(e)}")

    def create_notification(self, title, message, type='info', related_id=None, related_type=None):
        try:
            notification = Notification(
                title=title,
                message=message,
                type=type,
                related_id=related_id,
                related_type=related_type,
                is_read=False,
                db_manager=self.db_manager
            )

            success, error = notification.save()
            if not success:
                raise BusinessException(f"Не удалось создать уведомление: {error}")

            return notification
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при создании уведомления: {str(e)}")

    def mark_as_read(self, notification_id):
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
        try:
            today = datetime.now().strftime('%Y-%m-%d')

            query = """
                SELECT id, name, deadline
                FROM projects
                WHERE deadline <= ? AND deadline IS NOT NULL
                AND id NOT IN (
                    SELECT related_id FROM notifications 
                    WHERE related_type = 'project_overdue' AND related_id IS NOT NULL
                )
            """
            cursor = self.execute_query(query, [today])

            count = 0
            for row in cursor.fetchall():
                project_id = row[0]
                project_name = row[1]
                deadline = row[2]

                self.create_notification(
                    title="Просрочен дедлайн проекта",
                    message=f"Проект '{project_name}' просрочен. Дедлайн был {deadline}.",
                    type="warning",
                    related_id=project_id,
                    related_type="project_overdue"
                )
                count += 1

            return count
        except Exception as e:
            if isinstance(e, (BusinessException, ValidationException, DatabaseException)):
                raise e
            raise BusinessException(f"Ошибка при проверке просроченных проектов: {str(e)}")

    def check_upcoming_deadlines(self, days=3):
        try:
            today = datetime.now().date()
            future_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')

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
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

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
        try:
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
