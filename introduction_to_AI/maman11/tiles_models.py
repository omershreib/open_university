from typing import Tuple
from introduction_to_AI.models import to_vector

# action (row, col)
UP = to_vector(-1, 0)
DOWN = to_vector(+1, 0)
LEFT = to_vector(0, -1)
RIGHT = to_vector(0, +1)

TILES_ACTIONS = [UP, DOWN, LEFT, RIGHT]

tiles_actions_to_labels: dict = {str(UP): 'UP', str(DOWN): 'DOWN', str(LEFT): 'LEFT', str(RIGHT): 'RIGTH'}


class TileMovement:
    def __init__(self, tile_value, tile_pos, action):
        self.tile_value = tile_value
        self.tile_pos = tile_pos
        self.action = action

    @staticmethod
    def is_legal_point(x, y):
        return (0 <= x < 3) and (0 <= y < 3)

    def move(self):
        return to_vector(*(self.tile_pos + self.action))

    def target_pos(self):
        return self.move().tolist()

    def is_legal_pos(self):
        return self.is_legal_point(*self.tile_pos.data.tolist())

    def is_legal_move(self):
        return self.is_legal_point(*self.move().tolist())

    def pack(self):
        return self.tile_pos, self.action

    def todict(self):
        return {'tile_pos': self.tile_pos, 'action': self.action}

    def describe(self):
        return (f"tile_value: {self.tile_value}, curr_pos: {self.tile_pos}, target_pos: {self.target_pos()}, "
                f"action: {self.action}, action_description: {self._get_action_label(self.action)}")

    @staticmethod
    def _get_action_label(action: Tuple[int, int]) -> str:
        return tiles_actions_to_labels[str(action)]

    def __str__(self):
        return self.describe()

    def __repr__(self):
        return self.describe()
