from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
from introduction_to_AI.models import *
from introduction_to_AI.search_strategies import *


def reconstruct_actions_path(problem, path):
    """
    Convert a path of states into a list of TileMovement objects.

    Args:
        path: list of game states from start to goal

    Returns:
        list[TileMovement]
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
    def __init__(self, problem, algorithm_name):
        self.algorithm_name = algorithm_name
        self.problem = problem
        self.path_length = 0
        self.expanded_nodes = 0
        self.get_key = lambda x: str(x)

    def reconstruct_actions_path(self, path):
        return reconstruct_actions_path(self.problem, path)

    @property
    def algorithm_name(self) -> str:
        return self._algorithm_name

    @algorithm_name.setter
    def algorithm_name(self, name: str):
        self._algorithm_name = name

    @abstractmethod
    def build_actions_plan(self, state):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass


class HeuristicAgent(ABC):
    def __init__(self, problem: Problem, evaluator: Evaluator):
        self.problem = problem
        self.evaluator = evaluator
        self.goal_state = problem.goal_state
        self.expanded_nodes = 0

    def reconstruct_actions_path(self, path):
        return reconstruct_actions_path(self.problem, path)

    @abstractmethod
    def choose_move(self, state):
        pass

    def evaluate(self, curr_state):
        return self.evaluator.evaluate(curr_state, self.problem.goal_state)


class AStarAgent(HeuristicAgent):
    def __init__(self, problem, evaluator: Evaluator):
        super().__init__(problem, evaluator)

    def choose_move(self, state):
        self.problem.initial_state = state
        goal_node = self.search()
        return goal_node

    def search(self):
        def f(node):
            return node.path_cost + self.evaluator.evaluate(
                node.state, self.problem.goal_state
            )

        goal_node, self.expanded_nodes = best_first_search(self.problem, f)

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
