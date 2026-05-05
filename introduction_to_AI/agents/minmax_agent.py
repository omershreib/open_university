from __future__ import annotations

from abc import ABC
from introduction_to_AI.models import *
from introduction_to_AI.minmax_tree_utils import alphabeta_decision
# from introduction_to_AI.maman13 import *
from .heuristic_agent import HeuristicAgent


class MinMaxAgent(HeuristicAgent, ABC):
    def __init__(self, problem: Problem,
                 evaluator: Evaluator,
                 depth: int,
                 player: int):
        super().__init__(problem=problem, algorithm_name="", evaluator=evaluator)

        self.depth = depth
        self.player = player

    def choose_move(self, state: State) -> Move:
        return alphabeta_decision(self.problem, state, self.depth, self.evaluator)
