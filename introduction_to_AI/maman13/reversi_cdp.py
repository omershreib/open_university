from __future__ import annotations
from enum import Enum


class ColorDiskPlayer(Enum):
    RED = 1
    WHITE = -1

    def opponent(self) -> ColorDiskPlayer:
        return ColorDiskPlayer(-self.value)

    def __str__(self):
        return "R" if self == ColorDiskPlayer.RED else "W"

    def __repr__(self):
        return f"<ColorDiskPlayer: Color={self.value}>"
