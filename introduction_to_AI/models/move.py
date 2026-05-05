from __future__ import annotations

from abc import ABC, abstractmethod


class Move(ABC):

    @abstractmethod
    def is_pass(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def pass_move() -> Move:
        pass

    @abstractmethod
    def __eq__(self, other: Move):
        pass

    @abstractmethod
    def get_move(self):
        pass
