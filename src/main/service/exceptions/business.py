class BusinessException(Exception):
    def __init__(self, message="Ошибка бизнес-логики"):
        super().__init__(message)
