from __future__ import annotations
from abc import ABC, abstractmethod


class Evaluator(ABC):
    def __init__(self, problem):
        self.problem = problem
    
    @abstractmethod
    def evaluate(self, *args, **kwargs):
        pass



class ManhattanDistanceEvaluator(Evaluator, ABC):
    def evaluate(self, curr_state):
        pass
