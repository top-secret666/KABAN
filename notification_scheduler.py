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
            print(f"Создано уведомлений: {results['total']}")
            print(f"- Просроченные проекты: {results['overdue_projects']}")
            print(f"- Приближающиеся дедлайны: {results['upcoming_deadlines']}")
            print(f"- Неактивные задачи: {results['inactive_tasks']}")
            print(f"- Предупреждения о бюджете: {results['budget_warnings']}")
            return results
        except Exception as e:
            print(f"Ошибка при выполнении проверок уведомлений: {str(e)}")
            return {'total': 0}