from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from introduction_to_AI.models import *
from introduction_to_AI.common import make_node, expand
from introduction_to_AI.search_strategies import *


def reconstruct_actions_path(problem: Problem, path: list):
    """
    Convert a path of states into a list of action objects.

    Args:
        problem: a valid Problem object
        path: list of game states from initial state to a goal state

    Returns:
        an action lists that been induced by this path
    """
    if not path or len(path) < 2:
        return []

    actions = []

    for i in range(len(path) - 1):
        curr_state = path[i]
        next_state = path[i + 1]

        movement = problem.args_action(curr_state, next_state)
        actions.append(movement)

    return actions


class DeterministicAgent(ABC):
    """An Abstract Class for Deterministic Agent"""
    def __init__(self, problem: Problem, algorithm_name: str):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        """
        self.algorithm_name = algorithm_name
        self.problem = problem
        self.path_length = 0
        self.expanded_nodes = 0

    def reconstruct_actions_path(self, path) -> list:
        return reconstruct_actions_path(self.problem, path)

    @property
    def algorithm_name(self) -> str:
        return self._algorithm_name

    @algorithm_name.setter
    def algorithm_name(self, name: str):
        self._algorithm_name = name

    def solve(self, state: State):
        return self.build_actions_plan(state)

    @abstractmethod
    def build_actions_plan(self, state: State):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class HeuristicAgent(ABC):
    """An Abstract Class for Heuristic Agent"""
    def __init__(self, problem: Problem, algorithm_name: str, evaluator: Evaluator):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        :param evaluator: an Evaluator object that include a valid (consistent and admissible) evaluate() function
        """
        self.problem = problem
        self.algorithm_name = algorithm_name
        self.evaluator = evaluator
        self.goal_state = problem.goal_state

        # a counter for how many times this agent expand its nodes
        self.expanded_nodes = 0

    def reconstruct_actions_path(self, path):
        return reconstruct_actions_path(self.problem, path)

    @abstractmethod
    def choose_move(self, state):
        pass

    @abstractmethod
    def solve(self):
        pass

    def evaluate(self, curr_state):
        return self.evaluator.evaluate(curr_state, self.problem.goal_state)


class AStarAgent(HeuristicAgent):
    """A* Agent Class Object"""
    def __init__(self, problem, evaluator: Evaluator):
        """

        :param problem:
        :param evaluator:
        """
        super().__init__(problem, evaluator)

    def choose_move(self, state):
        self.problem.initial_state = state
        goal_node = self.search()
        return goal_node

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


class BFSAgent(DeterministicAgent):
    def __init__(self, problem: Problem):
        super().__init__(problem=problem, algorithm_name='BFS')

    def _run_setup(self, start_state):
        self.visited = set()
        self.queue = deque()
        self.parent = {}
        self.expanded_nodes = 0

        self.init_state = start_state
        self.queue.append((start_state, [start_state]))
        self.visited.add(start_state.get_key())

    def run(self, state):
        self._run_setup(state)

        if self.problem.is_goal_state(state):
            return state, []

        while self.queue:
            curr_state, path = self.queue.popleft()

            # increase number of expanded nodes
            self.expanded_nodes += 1

            for child in expand(self.problem, make_node(state=curr_state)):
                child_state = child.state
                key = child_state.get_key()

                if key not in self.visited:
                    self.visited.add(key)
                    self.parent[key] = child

                    if self.problem.is_goal_state(child_state):
                        path.append(child_state)
                        return child, path

                    self.queue.append((child_state, path + [child_state]))

        # in case of no solution
        return None, []

    def build_actions_plan(self, state):
        goal_state, path = self.run(state)
        if goal_state and len(path) == 0:
            return []

        actions = self.reconstruct_actions_path(path)
        return actions
