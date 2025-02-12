import abc


class Table(abc.ABC):

    @abc.abstractmethod
    def get(self) -> str:
        pass
