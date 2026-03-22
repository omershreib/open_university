from __future__ import annotations

from collections import deque
from introduction_to_AI.models import Problem, expand, make_node


class DeterministicAgent:
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name
        self.path_length = 0
        self.expanded_nodes = 0
        self.get_key = lambda x: str(x)

    @property
    def algorithm_name(self) -> str:
        return self._algorithm_name

    @algorithm_name.setter
    def algorithm_name(self, name: str):
        self._algorithm_name = name

    def build_actions_plan(self, state):
        raise NotImplementedError


    def run(self, *args, **kwargs):
        raise NotImplementedError


class BFSAgent(DeterministicAgent):
    def __init__(self, problem: Problem):
        super().__init__(algorithm_name='BFS')
        self.problem = problem

    def _run_setup(self, start_state):
        self.visited = set()
        self.queue = deque()
        self.parent = {}
        self.expanded_nodes = 0

        self.init_state = start_state
        self.queue.append((start_state, [start_state]))
        self.visited.add(start_state.get_key())

    def run(self, state):
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
        return None
