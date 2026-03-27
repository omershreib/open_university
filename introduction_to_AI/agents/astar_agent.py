from __future__ import annotations

from introduction_to_AI.search_strategies import *
from .heuristic_agent import HeuristicAgent


class AStarAgent(HeuristicAgent):
    """A* Agent Class Object"""

    def __init__(self, problem: Problem, algorithm_name: str, evaluator: Evaluator):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        :param evaluator: an Evaluator object that include a valid (consistent and admissible) evaluate() function
        """
        super().__init__(problem=problem, algorithm_name=algorithm_name, evaluator=evaluator)

    def solve(self, *args, **kwargs):
        return self.search()

    def search(self):
        def f(node):
            return node.path_cost + self.evaluator.evaluate(
                node.state, self.problem.goal_state
            )

        goal_node, self.expanded_nodes = best_first_search(self.problem, f, self.evaluator.evaluate)

        if not goal_node:
            return False

        return self.reconstruct_actions_path(
            self.reconstruct_state_path(goal_node))

    @staticmethod
    def reconstruct_state_path(goal_node):
        path = []
        curr = goal_node

        while curr is not None:
            path.append(curr.state)
            curr = curr.parent

        path.reverse()
        return path
