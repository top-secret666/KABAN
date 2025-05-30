from src.main.service.notification import NotificationService


class NotificationController:
    def __init__(self, service=None):
        super().__init__(service or NotificationService())

    def get_all_notifications(self, limit=None, offset=None, only_unread=False):
        return self.execute_service_method('get_all_notifications', limit, offset, only_unread)

    def get_notification_by_id(self, notification_id):
        return self.execute_service_method('get_notification_by_id', notification_id)

    def create_notification(self, title, message, type='info', related_id=None, related_type=None):
        return self.execute_service_method('create_notification', title, message, type, related_id, related_type)

    def mark_as_read(self, notification_id):
        return self.execute_service_method('mark_as_read', notification_id)

    def mark_all_as_read(self):
        return self.execute_service_method('mark_all_as_read')

    def delete_notification(self, notification_id):
        return self.execute_service_method('delete_notification', notification_id)

    def delete_all_read_notifications(self):
        return self.execute_service_method('delete_all_read_notifications')

    def check_overdue_projects(self):
        return self.execute_service_method('check_overdue_projects')

    def check_upcoming_deadlines(self, days=3):
        return self.execute_service_method('check_upcoming_deadlines', days)

    def check_inactive_tasks(self, days=7):
        return self.execute_service_method('check_inactive_tasks', days)

    def check_budget_warnings(self, threshold=0.8):
        return self.execute_service_method('check_budget_warnings', threshold)

    def run_all_checks(self):
        return self.execute_service_method('run_all_checks')
