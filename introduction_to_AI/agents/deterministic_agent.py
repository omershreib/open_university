from __future__ import annotations

from abc import ABC, abstractmethod
from introduction_to_AI.search_strategies import *
from introduction_to_AI.agents.common_agents_utils import reconstruct_actions_path
from .atomic_agent import AtomicAgent


class DeterministicAgent(AtomicAgent, ABC):
    """An Abstract Class for Deterministic Agent"""
    def __init__(self, problem: Problem, algorithm_name: str):
        """

        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param algorithm_name: a label name for this agent's algorithm
        """
        super().__init__(problem=problem, algorithm_name=algorithm_name)

        #self.path_length = 0
        self.expanded_nodes = 0

    def reconstruct_actions_path(self, path) -> list:
        return reconstruct_actions_path(self.problem, path)

    @property
    def algorithm_name(self) -> str:
        return self._algorithm_name

    @algorithm_name.setter
    def algorithm_name(self, name: str):
        self._algorithm_name = name

    def solve(self, state: State):
        return self.build_actions_plan(state)

    @abstractmethod
    def build_actions_plan(self, state: State):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        pass