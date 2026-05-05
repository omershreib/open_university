from introduction_to_AI.models.evaluator import Evaluator
from introduction_to_AI.maman13 import ReversiGameState, ColorDiskPlayer
from abc import ABC, abstractmethod


class ReversiEvaluator(Evaluator, ABC):
    pass


class ReversiScoreEvaluator(ReversiEvaluator):
    """Reversi Score Evaluator

    heuristic motivation:   maximize player's score in every move
    """

    def evaluate(self, state: ReversiGameState, player: ColorDiskPlayer) -> int:
        return state.score(player) - state.score(player.opponent())
