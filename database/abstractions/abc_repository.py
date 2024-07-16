from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def get(self, id):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def create(self, values: dict):
        raise NotImplementedError

    @abstractmethod
    def update(self, id, values: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
