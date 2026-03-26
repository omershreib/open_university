from __future__ import annotations

from abc import ABC, abstractmethod
class State(ABC):
    @abstractmethod
    def get_key(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
