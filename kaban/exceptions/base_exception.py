class KabanException(Exception):
    """
    Базовый класс для всех исключений в приложении KABAN Manager
    """
    def __init__(self, message="Произошла ошибка в приложении"):
        self.message = message
        super().__init__(self.message)
