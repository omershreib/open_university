from __future__ import annotations

from abc import ABC, abstractmethod


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, curr_state, goal_state):
        pass
