from abc import ABC, abstractmethod
from typing import Any


class IField(ABC):
    @abstractmethod
    def transform(self, value: Any):
        pass

    @abstractmethod
    def get_filters(self, value: Any):
        pass

    @abstractmethod
    def filter(self, value: Any):
        pass
