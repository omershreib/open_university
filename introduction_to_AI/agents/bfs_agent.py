from __future__ import annotations

from typing import Optional, List
from collections import deque
from introduction_to_AI.search_strategies import *
from .deterministic_agent import DeterministicAgent


class BFSAgent(DeterministicAgent):
    """BFS Agent Class Object

    applied on a valid problem object and attempt to solve it using the BFS algorithm
    """

    def __init__(self, problem: Problem):
        super().__init__(problem=problem, algorithm_name='BFS')

    def _run_setup(self, start_state):
        """BFS running setup

        prepare the visited set, the FIFO queue and the parent nodes dictionary
        required to be initialized before starting BFS graph search

        :param start_state:
        :return:
        """
        self.visited = set()
        self.queue = deque()
        self.parent = {}

        # initiate expanded-nodes (in case of using this agent multiple times)
        self.expanded_nodes = 0

        self.init_state = start_state
        self.queue.append((start_state, [start_state]))
        self.visited.add(start_state.get_key())

    def run(self, state: State):
        """Run BFS on this state

        implemented EXACTLY as described in the course book (page 95)

        Args:
            state: a valid state object (should be the initial state)

        Return:
            if found a solution (iff, found a path to a goal state)
            then returns a pair of (goal-state, path-from-init-to-goal)

            otherwise, returns (None, empty-list)
        """
        self._run_setup(state)

        if self.problem.is_goal_state(state):
            return state, []

        while self.queue:
            curr_state, path = self.queue.popleft()

            # increase number of expanded nodes
            self.expanded_nodes += 1

            for child in expand(self.problem, make_node(state=curr_state)):
                child_state = child.state
                key = child_state.get_key()

                if key not in self.visited:
                    self.visited.add(key)
                    self.parent[key] = child

                    if self.problem.is_goal_state(child_state):
                        path.append(child_state)
                        return child, path

                    self.queue.append((child_state, path + [child_state]))

        # in case of no solution
        return None, []

    def build_actions_plan(self, state: State) -> Optional[List]:
        """Action Plan Builder

        if the BFS algorithm (applied by the run() method) returns a goal-state and a path
        then build an ordered list of actions objects that create this states-path from
        the initial-state towards this goal-state

        Args:
            state: a valid state object (should be the initial state)

        Returns:
            if the problem is solvable, then returns an ordered action list
            otherwise, returns an empty-list
        """
        goal_state, path = self.run(state)
        if goal_state and len(path) == 0:
            return []

        actions = self.reconstruct_actions_path(path)
        return actions
