"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from __future__ import annotations

from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def get_key(self):
        pass

    @abstractmethod
    def get_value(self):
        pass

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
