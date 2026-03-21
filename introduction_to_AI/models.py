from __future__ import annotations
import numpy as np

to_vector = lambda x, y: np.array([x, y])

class Problem:
    def __init__(self, *args, **kwargs):
        self.states: list = []
        self.initial_state = None
        self.actions = None
        self.transition_model = None
        self.goal_state = None
        self.action_cost = None

    def get_actions(self, state):
        raise NotImplementedError

    def update(self, state, action) -> None:
        raise NotImplementedError

    def is_goal_state(self, state):
        raise NotImplementedError

    @staticmethod
    def _is_legal_action(state):
        raise NotImplementedError


class Node:
    def __init__(self, state, parent, action, path_cost, label=None):
        self.state = state
        self.parent = parent
        self.action = action  # the action that was applied to the parent's state to generate this node
        self.path_cost = path_cost  # the total cost of the path from the initial state to this node
        self.label = label

    def __str__(self):
        # label name to identify this node in the lookup table
        return self.label


def make_node(*args, **kwargs):
    # a constructor for Node object creation
    state = None
    patent = None
    action = None
    label = ''

    if 'state' in kwargs.keys():
        state = kwargs.get('state')

    if 'parent' in kwargs.keys():
        parent = kwargs.get('parent')

    if 'action' in kwargs.keys():
        action = kwargs.get('action')

    if 'label' in kwargs.keys():
        label = kwargs.get('label')

    return Node(state=state, parent=parent, action=action, label=label)
