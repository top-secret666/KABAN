from abc import ABC, abstractmethod


class BaseModel(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass

    @abstractmethod
    def validate(self):
        pass