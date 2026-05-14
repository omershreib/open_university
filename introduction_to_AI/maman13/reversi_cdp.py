"""
Author: Omer Shraibshtein (205984271)
Date:   14/05/2026
Email:  omershreib@gmail.com
"""

from __future__ import annotations
from enum import Enum

# CDP refers to Control Disk Player
class ColorDiskPlayer(Enum):
    RED = 1
    WHITE = -1

    def opponent(self) -> ColorDiskPlayer:
        return ColorDiskPlayer(-self.value)

    def __str__(self):
        return "R" if self == ColorDiskPlayer.RED else "W"

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value

    def __repr__(self):
        return f"<ColorDiskPlayer: Color={self.value}>"
