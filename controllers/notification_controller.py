from controllers.base_controller import BaseController
from services.notification_service import NotificationService

class NotificationController(BaseController):
    """
    Контроллер для управления уведомлениями
    """
    def __init__(self, service=None):
        """
        Инициализирует контроллер с сервисом уведомлений
        """
        super().__init__(service or NotificationService())
    
    def get_all_notifications(self, limit=None, offset=None, only_unread=False):
        """
        Получает список всех уведомлений
        """
        try:
            result = self.execute_service_method('get_all_notifications', limit, offset, only_unread)
            print(f"Получено уведомлений: {len(result['data']) if result['success'] and 'data' in result else 0}")
            return result
        except Exception as e:
            print(f"Ошибка при получении уведомлений: {str(e)}")
            return {'success': False, 'error': str(e), 'data': []}

    def get_notification_by_id(self, notification_id):
        """
        Получает уведомление по ID
        """
        return self.execute_service_method('get_notification_by_id', notification_id)
    
    def create_notification(self, title, message, type='info', related_id=None, related_type=None):
        """
        Создает новое уведомление
        """
        return self.execute_service_method('create_notification', title, message, type, related_id, related_type)
    
    def mark_as_read(self, notification_id):
        """
        Отмечает уведомление как прочитанное
        """
        return self.execute_service_method('mark_as_read', notification_id)
    
    def mark_all_as_read(self):
        """
        Отмечает все уведомления как прочитанные
        """
        return self.execute_service_method('mark_all_as_read')
    
    def delete_notification(self, notification_id):
        """
        Удаляет уведомление
        """
        return self.execute_service_method('delete_notification', notification_id)
    
    def delete_all_read_notifications(self):
        """
        Удаляет все прочитанные уведомления
        """
        return self.execute_service_method('delete_all_read_notifications')
    
    def check_overdue_projects(self):
        """
        Проверяет просроченные проекты и создает уведомления
        """
        return self.execute_service_method('check_overdue_projects')
    
    def check_upcoming_deadlines(self, days=3):
        """
        Проверяет приближающиеся дедлайны и создает уведомления
        """
        return self.execute_service_method('check_upcoming_deadlines', days)
    
    def check_inactive_tasks(self, days=7):
        """
        Проверяет неактивные задачи и создает уведомления
        """
        return self.execute_service_method('check_inactive_tasks', days)
    
    def check_budget_warnings(self, threshold=0.8):
        """
        Проверяет проекты с превышением бюджета и создает уведомления
        """
        return self.execute_service_method('check_budget_warnings', threshold)
    
    def run_all_checks(self):
        """
        Запускает все проверки и создает уведомления
        """
        return self.execute_service_method('run_all_checks')
