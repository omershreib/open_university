from introduction_to_AI.models.evaluator import Evaluator
from introduction_to_AI.maman13.reversi_game_state import ReversiGameState
from introduction_to_AI.maman13.reversi_cdp import ColorDiskPlayer
from abc import ABC

"""
Author: Omer Shraibshtein (205984271)
Date:   14/05/2026
Email:  omershreib@gmail.com
"""
class ReversiEvaluator(Evaluator, ABC):
    pass


class ReversiScoreEvaluator(ReversiEvaluator):
    """Reversi Score Evaluator

    heuristic motivation:   maximize player's score in every move
    """

    def evaluate(self, state: ReversiGameState, player: ColorDiskPlayer) -> int:
        return state.score(player) - state.score(player.opponent())
