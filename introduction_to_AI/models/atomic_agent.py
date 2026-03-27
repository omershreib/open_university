from abc import ABC, abstractmethod
from introduction_to_AI.models import Problem, State


class AtomicAgent(ABC):
    def __init__(self, problem: Problem, algorithm_name: str):
        self.algorithm_name = algorithm_name
        self.problem = problem

    @abstractmethod
    def choose_move(self, state: State):
        pass

    @abstractmethod
    def solve(self, *args, **kwargs):
        pass
