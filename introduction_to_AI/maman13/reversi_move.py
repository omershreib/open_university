from __future__ import annotations

from typing import Optional
from introduction_to_AI.models import Move


class ReversiMove(Move):
    def __init__(self, row: Optional[int], column: Optional[int]):
        self.row = row
        self.column = column

    @property
    def is_pass(self) -> bool:
        return self.row is None and self.column is None

    @staticmethod
    def pass_move() -> ReversiMove:
        return ReversiMove(None, None)

    def __eq__(self, other: ReversiMove):
        return self.get_move() == other.get_move()

    def get_move(self):
        return self.row, self.column

    def __str__(self) -> str:
        return "PASS" if self.is_pass else f"({self.row},{self.column})"

    def __repr__(self):
        return f"Move{self.get_move()}"
