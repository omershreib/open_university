from __future__ import annotations
import random
import numpy as np
from introduction_to_AI.common import vector


class TilesBoard:
    def __init__(self, board_config: list = None, random_board=False, size=3):
        """

        :param board_config: 2-dimensional list in the shape of (n,n) depicts a tiles board configuration
            for example (n=3) board_confing = [[1,4,0],[5,8,2],[3,6,7]]

        :param random_board: if true, create a random board configuration
                WARNING! not every random configuration is solvable

        :param size: the shape of the board (by default 3, which is the "classic" 3 x 3 Tiles board)
        """
        self.__empty_symbol = 0
        self.__size = size
        if board_config is not None:
            self.board = board_config

        if random_board:
            self.board = np.full((size, size), self.empty_symbol, dtype=np.uint8)
            self.generate_random_init_state()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board_config: list):
        self._board = np.array(board_config, dtype=np.uint8)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def empty_symbol(self):
        return self.__empty_symbol

    @empty_symbol.setter
    def empty_symbol(self, value):
        self.__empty_symbol = value

    def __tile_upper_bound(self):
        return self.size ** 2

    def args_tile_pos(self, i) -> tuple:
        tile_last_value: int = self.__tile_upper_bound() - 1
        assert 0 < i < self.__tile_upper_bound(), f"tile number must be between 0 and {tile_last_value} (received {i})"
        return tuple(np.argwhere(self.board == i)[0])

    def get_tile_pos(self, x, y):
        n = self.size
        assert (0 <= x < n) and (0 <= y < n), (f"tile position must be between (0,0) to ({n - 1},{n - 1}) "
                                               f"(received (({x},{y})))")
        return self.board[*vector(x, y)]

    def generate_random_init_state(self):
        # game_tiles: list = [self.empty_symbol, 1, 2, 3, 4, 5, 6, 7, 8]
        n: int = self.size
        game_tiles: list = list(range(1, self.__tile_upper_bound() - 1))
        game_tiles.append(self.empty_symbol)
        random.shuffle(game_tiles)
        start = 0
        end = n

        for i in range(n):
            self.board[i,] = game_tiles[start: end]
            start = end
            end += n

    def move_tile(self, tile_pos, direction) -> TilesBoard:
        new_tile_pos = vector(*tile_pos) + vector(*direction)
        board = self.board.copy()

        if board[*new_tile_pos] == self.empty_symbol:
            tile_value = board[*tile_pos]
            board[*tile_pos] = self.empty_symbol
            board[*new_tile_pos] = tile_value
            return TilesBoard(board_config=board.tolist())

        raise Exception("tile move is not allowed")

    def _display(self):
        print()             # add a newline gap
        n = self.size
        for row in range(n):
            row_display = ""
            for col in range(n):
                tile = self.board[row, col]
                row_display += f" {tile}"

            print(row_display)
