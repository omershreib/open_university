from game_board import ReversiGameBoard
from models import Color, Move


class GameState:
    def __init__(self, board: ReversiGameBoard, player_turn: Color):
        self.board = board
        self.player_turn = player_turn
        self.consecutive_passes: int = 0

    def actions(self) -> list[Move]:
        return self.board.legal_moves(self.player_turn)

    def movement_result(self, move: Move) -> "GameState":
        updated_board = self.board.apply_player_move(self.player_turn, move)
        return GameState(updated_board, self.player_turn.opposition())

    def is_terminal(self) -> bool:
        return self.consecutive_passes >= 2 or self.board.is_full()
