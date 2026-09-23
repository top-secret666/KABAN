from exceptions.base_exception import KabanException

class BusinessException(KabanException):
    """
    Исключение, возникающее при ошибках бизнес-логики
    """
    def __init__(self, message="Ошибка бизнес-логики"):
        super().__init__(message)
