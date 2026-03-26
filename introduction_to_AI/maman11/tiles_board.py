from __future__ import annotations
import random
import numpy as np
from introduction_to_AI.common import vector


class TilesBoard:
    def __init__(self, board_config: list = None, random_board=False):
        self.empty_pos_value = 0
        if board_config is not None:
            self.board = board_config

        if random_board:
            self.board = np.full((3, 3), self.empty_pos_value, dtype=np.uint8)
            self.generate_random_init_state()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board_config: list):
        self._board = np.array(board_config, dtype=np.uint8)

    def args_tile_pos(self, i) -> tuple:
        assert 0 < i < 9, f"tile number must be between 0 and 8 (received {i})"
        return tuple(np.argwhere(self.board == i)[0])

    def get_tile_pos(self, x, y):
        assert (0 <= x < 3) and (0 <= y < 3), f"tile position must be between (0,0) to (2,2) (received (({x},{y})))"
        return self.board[*vector(x, y)]

    def generate_random_init_state(self):
        game_tiles: list = [self.empty_pos_value, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(game_tiles)

        first_row = game_tiles[:3]
        second_row = game_tiles[3:6]
        third_row = game_tiles[6:]

        self.board[0,] = first_row
        self.board[1,] = second_row
        self.board[2,] = third_row

    def move_tile(self, tile_pos, direction) -> TilesBoard:
        new_tile_pos = vector(*tile_pos) + vector(*direction)
        board = self.board.copy()

        if board[*new_tile_pos] == self.empty_pos_value:
            tile_value = board[*tile_pos]
            board[*tile_pos] = self.empty_pos_value
            board[*new_tile_pos] = tile_value
            return TilesBoard(board_config=board.tolist())

        raise Exception("tile move is not allowed")

    def display(self):
        print("display current tiles game stage")
        for row in range(3):
            row_display = ""
            for col in range(3):
                tile = self.board[row, col]
                row_display += f" {tile}"

            print(row_display)