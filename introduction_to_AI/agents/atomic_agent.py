"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from abc import ABC, abstractmethod
from introduction_to_AI.models import Problem


class AtomicAgent(ABC):
    """Atomic Agent Class Object

    I called this "atomic-agent" (instead of just called it "agent") in order to emphasize
    that it is the agent kernel that any other agent must have.

    In details, any agent (either heuristic or deterministic) must have:
        - the name of the algorithm it uses
        - the problem it attempts to deal with
        - the number of times the expand() method had been called during this agent's solution
            attempt's lifetime (from initial-state toward a goal-state)
        - a `solve()` method (must be overwritten by a sub-agent class)

    """
    def __init__(self, problem: Problem, algorithm_name: str):
        self.algorithm_name = algorithm_name
        self.problem = problem

        # a counter for how many times this agent expand its nodes
        self.expanded_nodes = 0

    @abstractmethod
    def solve(self, *args, **kwargs):
        pass
