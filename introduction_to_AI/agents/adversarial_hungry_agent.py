from .atomic_agent import AtomicAgent
from introduction_to_AI.models import *
from abc import ABC, abstractmethod


class AdversarialHungryAgent(AtomicAgent, ABC):
    def __init__(self, problem: Problem):
        super().__init__(problem=problem, algorithm_name="")

    @abstractmethod
    def choose_move(self, state: State):
        pass
