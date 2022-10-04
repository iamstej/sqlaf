from abc import ABC, abstractmethod


class IFilter(ABC):

    _query = None
    _raise_exceptions = True

    def __init__(self, query, raise_exceptions=False):
        self._query = query
        self._raise_exceptions = raise_exceptions

    @abstractmethod
    def filter(self):
        pass
