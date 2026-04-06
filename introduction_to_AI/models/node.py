"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from __future__ import annotations


class Node:
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action  # the action that was applied to the parent's state to generate this node
        self.path_cost = path_cost  # the total cost of the path from the initial state to this node

    def __lt__(self, other: Node):
        return self.path_cost < other.path_cost