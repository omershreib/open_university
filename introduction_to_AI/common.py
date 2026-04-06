"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from __future__ import annotations

from introduction_to_AI.models.node import Node
from introduction_to_AI.models.problem import Problem
import heapq as pq
import queue
import numpy as np


def vector(x: int, y: int) -> np.array:
    return np.array([x, y])


def make_node(state, parent=None, action=None, path_cost=1) -> Node:
    # a constructor for Node object creation

    return Node(state=state, parent=parent, action=action, path_cost=path_cost)


def expand(problem: Problem, node: Node):
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


def is_empty(lst):
    return len(lst) == 0


def pop(frontier):
    return pq.heappop(frontier)


def top(frontier):
    return frontier[0]


def push(frontier, values):
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

    return lst
