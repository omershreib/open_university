"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from __future__ import annotations

from abc import ABC, abstractmethod


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