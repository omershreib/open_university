from __future__ import annotations

from abc import ABC, abstractmethod
from introduction_to_AI.search_strategies import *
from introduction_to_AI.agents.common_agents_utils import reconstruct_actions_path


class HeuristicAgent(AtomicAgent, ABC):
    """An Abstract Class for Heuristic Agent"""

    def __init__(self, problem: Problem, algorithm_name: str, evaluator: Evaluator):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        :param evaluator: an Evaluator object that include a valid (consistent and admissible) evaluate() function
        """
        super().__init__(problem=problem, algorithm_name=algorithm_name)

        self.evaluator = evaluator
        self.goal_state = problem.goal_state

    def reconstruct_actions_path(self, path):
        return reconstruct_actions_path(self.problem, path)

    # @abstractmethod
    # def choose_move(self, state):
    #     pass

    @abstractmethod
    def solve(self):
        pass

    def evaluate(self, curr_state):
        return self.evaluator.evaluate(curr_state, self.problem.goal_state)
