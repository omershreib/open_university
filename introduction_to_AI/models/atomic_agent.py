from abc import ABC, abstractmethod
from introduction_to_AI.models import Problem


class AtomicAgent(ABC):
    def __init__(self, problem: Problem, algorithm_name: str):
        self.algorithm_name = algorithm_name
        self.problem = problem

        # a counter for how many times this agent expand its nodes
        self.expanded_nodes = 0

    @abstractmethod
    def solve(self, *args, **kwargs):
        pass
