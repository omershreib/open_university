import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from enum import Enum


class Color(Enum):
    RED = 1
    WHITE = -1

    def opposition(self):
        return Color(-self.value)


class Move:
    def __init__(self):
        self.horizontal: int | None = None
        self.vertical: int | None = None

    @property
    def is_pass(self):
        return self.horizontal is None


