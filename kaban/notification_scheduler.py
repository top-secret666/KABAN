from services.notification_service import NotificationService

class NotificationScheduler:
    """
    Планировщик для автоматической проверки и создания уведомлений
    """
    def __init__(self):
        self.notification_service = NotificationService()

    def run_checks(self):
        """
        Запускает все проверки для создания уведомлений
        """
        try:
            results = self.notification_service.run_all_checks()
            return results
        except Exception as e:
            return {'total': 0}
