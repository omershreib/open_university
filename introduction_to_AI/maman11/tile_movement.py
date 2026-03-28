from typing import Tuple
from introduction_to_AI.common import vector

# action (row, col)
UP = vector(-1, 0)
DOWN = vector(+1, 0)
LEFT = vector(0, -1)
RIGHT = vector(0, +1)

TILES_DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

tiles_directions_to_labels: dict = {str(UP): 'UP', str(DOWN): 'DOWN', str(LEFT): 'LEFT', str(RIGHT): 'RIGHT'}
labels_to_directions: dict = {'UP': UP, 'DOWN': DOWN, 'LEFT': LEFT, 'RIGHT': RIGHT}

class TileMovement:
    """Tile Movement Class Object

    in Tiles, the "action" is defined by the movement of a specific tile on the board,
    which includes:
        - the current coordinate position of the `i` tile
        - the current coordinate position of the empty place (defined in this program by 0)
        - the legal direction from the current `i` tile's position which cause a swap between
            the empty place with this `i` tile place.
    """
    def __init__(self, tile_value, tile_pos, direction, bound: int=3):
        """

        :param tile_value: integer between 1 and 8
        :param tile_pos: a `np.array` object [`int` `int`] (the coordinate of the `i` tile (0<i<9) on the board)
        :param direction: a (`int`, `int`) tuple depicting the tile movement: UP, DOWN, LEFT, or RIGHT
        :param bound: `int` represents the upper vertical/horizontal bound (always equals to board.size)
        """
        self.tile_value = tile_value
        self.tile_pos = tile_pos
        self.direction = direction
        self.bound = bound

    def is_legal_point(self, x, y):
        return (0 <= x < self.bound) and (0 <= y < self.bound)

    def move(self):
        return vector(*(self.tile_pos + self.direction))

    def target_pos(self):
        return self.move().tolist()

    def is_legal_pos(self):
        return self.is_legal_point(*self.tile_pos.data.tolist())

    def is_legal_move(self):
        return self.is_legal_point(*self.move().tolist())

    def pack(self):
        return self.tile_pos, self.direction

    def todict(self):
        return {'tile_pos': self.tile_pos, 'action': self.direction}

    def describe(self):
        return (f"tile_value: {self.tile_value}, curr_pos: {self.tile_pos}, target_pos: {self.target_pos()}, "
                f"direction: {self.direction}, action_description: {self._get_direction_label(self.direction)}")

    @staticmethod
    def _get_direction_label(direction: Tuple[int, int]) -> str:
        return tiles_directions_to_labels[str(direction)]

    def __str__(self):
        return self.describe()

    def __repr__(self):
        return self.describe()
