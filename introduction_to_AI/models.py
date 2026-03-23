from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

import numpy as np

to_vector = lambda x, y: np.array([x, y])


class Problem(ABC):
    def __init__(self, *args, **kwargs):
        self.states: list = []
        self.initial_state = None
        self.actions = None
        self.transition_model = None
        self.goal_state = None

    def get_actions(self, state):
        raise NotImplementedError

    def update(self, state, action) -> None:
        raise NotImplementedError

    def is_goal_state(self, state):
        raise NotImplementedError

    def action_cost(self, node, action, result_state):
        return node.path_cost + 1

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

    # def __str__(self):
    #     # label name to identify this node in the lookup table
    #     return self.state.get_key()


def make_node(state, parent=None, action=None, path_cost=1) -> Node:
    # a constructor for Node object creation
    return Node(state=state, parent=parent, action=action, path_cost=path_cost)


def expand(problem, node) -> Iterable:
    node_state = node.state

    for action in problem.get_actions(node_state):
        result_state = problem.update(node_state, action)
        cost = node.path_cost + problem.action_cost(node_state, action, result_state)

        yield Node(
            state=result_state,
            parent=node,
            action=action,
            path_cost=cost)
