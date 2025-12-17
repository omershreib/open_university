from __future__ import annotations
from models import ColorDiscPlayer
from game_state import GameState


class Evaluator:
    def evaluate(self, state: GameState, player: ColorDiscPlayer) -> int:
        raise NotImplementedError


class ScoreEvaluator(Evaluator):
    """Score Evaluator

    heuristic motivation:   maximize player's score in every move
    """
    def evaluate(self, state: GameState, player: ColorDiscPlayer) -> int:
        return state.board.calc_score(player) - state.board.calc_score(player.opposition())


class MobilityEvaluator(Evaluator):
    """Mobility Evaluator

    heuristic motivation:   minimize opposition player's number of legal moves in every move.
                            fundamental assumption is that when minimizing opposition's movements,
                            we reduce the number of moves that might cause the opposition to win.
    """
    def evaluate(self, state: GameState, player: ColorDiscPlayer) -> int:
        num_of_player_moves = len(state.board.legal_moves(player, include_pass=False))
        num_of_oppo_player_moves = len(state.board.legal_moves(player.opposition(), include_pass=False))
        return num_of_player_moves - num_of_oppo_player_moves


# class WeightedEvaluator(Evaluator):
#     """
#     Solid default: mobility + disc diff (you can extend with corners / weights later)
#     """
#     def __init__(self, w_mobility: float = 3.0, w_disc: float = 1.0):
#         self.w_m = w_mobility
#         self.w_d = w_disc
# 
#     def evaluate(self, state: GameState, player: ColorDiscPlayer) -> float:
#         player_score = state.board.calc_score(player) - state.board.calc_score(player.opposition())
#         mob = len(state.board.legal_moves(player, include_pass=False)) - \
#               len(state.board.legal_moves(player.opposition(), include_pass=False))
#         return self.w_m * mob + self.w_d * player_score
