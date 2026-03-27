from __future__ import annotations

from typing import Optional, List
from abc import ABC, abstractmethod
from collections import deque
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


class DeterministicAgent(AtomicAgent, ABC):
    """An Abstract Class for Deterministic Agent"""
    def __init__(self, problem: Problem, algorithm_name: str):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        """
        super().__init__(problem=problem, algorithm_name=algorithm_name)

        #self.path_length = 0
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


class AStarAgent(HeuristicAgent):
    """A* Agent Class Object"""
    def __init__(self, problem: Problem, algorithm_name: str, evaluator: Evaluator):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        :param evaluator: an Evaluator object that include a valid (consistent and admissible) evaluate() function
        """
        super().__init__(problem=problem, algorithm_name=algorithm_name, evaluator=evaluator)

    # todo: check if need this
    # def choose_move(self, state):
    #     self.problem.initial_state = state
    #     goal_node = self.search()
    #     return goal_node

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
    """BFS Agent Class Object

    applied on a valid problem object and attempt to solve it using the BFS algorithm
    """
    def __init__(self, problem: Problem):
        super().__init__(problem=problem, algorithm_name='BFS')

    def _run_setup(self, start_state):
        """BFS running setup

        prepare the visited set, the FIFO queue and the parent nodes dictionary
        required to be initialized before starting BFS graph search

        :param start_state:
        :return:
        """
        self.visited = set()
        self.queue = deque()
        self.parent = {}

        # initiate expanded-nodes (in case of using this agent multiple times)
        self.expanded_nodes = 0

        self.init_state = start_state
        self.queue.append((start_state, [start_state]))
        self.visited.add(start_state.get_key())

    def run(self, state: State):
        """Run BFS on this state

        implemented EXACTLY as described in the course book (page 95)

        Args:
            state: a valid state object (should be the initial state)

        Return:
            if found a solution (iff, found a path to a goal state)
            then returns a pair of (goal-state, path-from-init-to-goal)

            otherwise, returns (None, empty-list)
        """
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

    def build_actions_plan(self, state: State) -> Optional[List]:
        """Action Plan Builder

        if the BFS algorithm (applied by the run() method) returns a goal-state and a path
        then build an ordered list of actions objects that create this states-path from
        the initial-state towards this goal-state

        Args:
            state: a valid state object (should be the initial state)

        Returns:
            if the problem is solvable, then returns an ordered action list
            otherwise, returns an empty-list
        """
        goal_state, path = self.run(state)
        if goal_state and len(path) == 0:
            return []

        actions = self.reconstruct_actions_path(path)
        return actions
