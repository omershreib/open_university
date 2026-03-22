from __future__ import annotations
import random
import numpy as np
from introduction_to_AI.models import to_vector


SEED = 8
random.seed(SEED)


class TilesBoard:
    def __init__(self, board=None):
        self.empty_pos_value = 0
        if board is not None:
            self.board = np.array(board, dtype=np.uint8)

        else:
            self.board = np.full((3, 3), self.empty_pos_value, dtype=np.uint8)
            self.generate_random_init_state()
            
        

    def generate_random_init_state(self):
        game_tiles: list = [self.empty_pos_value, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(game_tiles)

        first_row = game_tiles[:3]
        second_row = game_tiles[3:6]
        third_row = game_tiles[6:]

        self.board[0,] = first_row
        self.board[1,] = second_row
        self.board[2,] = third_row

    def move_tile(self, tile_pos, action) -> TilesBoard:
        new_tile_pos = to_vector(*tile_pos) + to_vector(*action)

        board = self.board.copy()

        if board[*new_tile_pos] == self.empty_pos_value:
            tile_value = board[*tile_pos]
            board[*tile_pos] = self.empty_pos_value
            board[*new_tile_pos] = tile_value
            return TilesBoard(board=board.tolist())

        raise Exception("tile move is not allowed")

    def display(self):
        print("display current tiles game stage")
        for row in range(3):
            row_display = ""
            for col in range(3):
                tile = self.board[row, col]
                row_display += f" {tile}"

            print(row_display)


if __name__ == '__main__':
    board = TilesBoard()
    board.display()

    # move 7 tile in [1,1] left -> [1,0]
    # action needed [0,-1]
    tile_pos = [1, 1]
    action = [0, -1]
    board.move_tile(tile_pos, action)
    board.display()
