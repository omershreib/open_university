"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from __future__ import annotations

from abc import ABC, abstractmethod


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, curr_state, goal_state):
        pass
