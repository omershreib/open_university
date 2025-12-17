from __future__ import annotations
from typing import List
from models import ColorDiscPlayer, Move
from game_board import ReversiGameBoard


class GameState:
    def __init__(self, board: ReversiGameBoard, player_turn: ColorDiscPlayer, consecutive_passes: int = 0):
        self.board = board
        self.player_turn = player_turn
        self.consecutive_passes = consecutive_passes

    def actions(self) -> List[Move]:
        return self.board.legal_moves(self.player_turn, include_pass=True)

    def movement_result(self, move: Move) -> GameState:
        updated_board = self.board.apply_move(self.player_turn, move)
        new_passes = self.consecutive_passes + 1 if move.is_pass else 0
        return GameState(board=updated_board, player_turn=self.player_turn.opposition(), consecutive_passes=new_passes)

    def is_terminal(self) -> bool:
        # Terminal when both players have no moves => two consecutive passes,
        # or board full (redundant but fine).
        return self.consecutive_passes >= 2 or self.board.count_empty_cells() == 0
