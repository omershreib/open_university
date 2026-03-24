from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

import heapq as pq
import queue
import numpy as np

#to_vector = lambda x, y: np.array([x, y])


def vector(x: int, y: int) -> np.array:
    return np.array([x, y])


class Problem(ABC):
    def __init__(self, *args, **kwargs):
        self.states: list = []
        self.initial_state = None
        self.actions = None
        self.transition_model = None
        self.goal_state = None

    @abstractmethod
    def get_actions(self, state):
        pass

    @abstractmethod
    def update(self, state, action) -> None:
        pass

    @abstractmethod
    def is_goal_state(self, state):
        pass

    @abstractmethod
    def action_cost(self, curr_state, action, result_state):
        pass

    @abstractmethod
    def args_action(self, curr_state, next_state):
        pass

    @staticmethod
    def _is_legal_action(state):
        raise NotImplementedError


class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action  # the action that was applied to the parent's state to generate this node
        self.path_cost = path_cost  # the total cost of the path from the initial state to this node

    def __lt__(self, other: Node):
        return self.path_cost < other.path_cost


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, curr_state, goal_state):
        pass


def make_node(state, parent=None, action=None, path_cost=1) -> Node:
    # a constructor for Node object creation
    depth = 0
    if parent:
        depth = parent.depth + 1

    return Node(state=state, parent=parent, action=action, path_cost=path_cost)


def expand(problem, node):
    for action in problem.get_actions(node.state):
        result_state = problem.update(node.state, action)
        step_cost = problem.action_cost(node.state, action, result_state)
        total_cost = node.path_cost + step_cost

        yield Node(
            state=result_state,
            parent=node,
            action=action,
            path_cost=total_cost,
        )

def old_expand(problem, node) -> Iterable[Node]:
    node_state = node.state

    for action in problem.get_actions(node_state):
        result_state = problem.update(node_state, action)
        total_cost = node.depth + problem.action_cost(node_state, action, result_state)

        yield Node(
            state=result_state,
            parent=node,
            action=action,
            path_cost=total_cost)


def is_empty(lst):
    return len(lst) == 0


def pop(frontier):
    return pq.heappop(frontier)


def top(frontier):
    return frontier[0]


def add(frontier, values):
    pq.heappush(frontier, values)


def initiate_fifo_queue(iterable, f):
    q = queue.Queue()
    for item in sorted(iterable, key=lambda x: f(x)):
        q.put(item)

    return q


def build_priority_queue(iterable, f) -> list:
    # create a minimum heap ordered by
    # the order of the given iterable provided by a function f
    lst = []
    for item in sorted(iterable, key=lambda x: f(x)):
        pq.heappush(lst, item)

    # print(lst)
    return lst
