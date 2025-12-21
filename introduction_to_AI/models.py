from __future__ import annotations
from typing import Optional
from enum import Enum


class ColorDiscPlayer(Enum):
    RED = 1
    WHITE = -1

    def opponent(self) -> ColorDiscPlayer:
        return ColorDiscPlayer(-self.value)

    def __str__(self):
        return "R" if self == ColorDiscPlayer.RED else "W"


class Move:
    def __init__(self, row: Optional[int], column: Optional[int]):
        self.row = row
        self.column = column

    @property
    def is_pass(self) -> bool:
        return self.row is None and self.column is None

    @staticmethod
    def pass_move() -> Move:
        return Move(None, None)

    def __eq__(self, other: Move):
        return self.get_move() == other.get_move()

    def get_move(self):
        return self.row, self.column

    def __str__(self) -> str:
        return "PASS" if self.is_pass else f"({self.row},{self.column})"

    def __repr__(self):
        return f"Move{self.get_move()}"


if __name__ == '__main__':
    import sys

    red = ColorDiscPlayer.RED
    white = ColorDiscPlayer.WHITE
    print(sys.getsizeof(red))
    print(sys.getsizeof(white))
    # move_1 = Move(1, 2)
    # move_2 = Move(3, 4)
    # move_3 = Move(3, 4)
    #
    # print(move_2 in [move_1, move_3])
