from __future__ import annotations

from introduction_to_AI.agents import DeterministicAgent
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tiles_models import TilesGameProblem
from collections import deque
from pprint import pprint


class BFSAgent(DeterministicAgent):
    def __init__(self, problem: TilesGameProblem):
        self.problem = problem
        self.visited = set()
        self.queue = deque()
        self.parent = {}

    def init_queue_with_start_state(self, start_state):
        print("add start state into queue")
        self.queue.append(start_state)
        self.visited.add(start_state)

    def run_bfs(self, state: TilesGameState):
        self.init_queue_with_start_state(state)
        print(state.get_tiles_board().display())

        while self.queue:
            curr_state = self.queue.popleft()

            if self.problem.is_goal_state(state=curr_state):
                #return self.reconstruct_path(curr_state)
                pprint(self.parent)
                return True


            actions = self.problem.get_actions(curr_state)
            for action in actions:
                action_state = self.problem.update(curr_state, action)
                #action_state.get_tiles_board().display()

                key = str(action_state.get_board())
                value = f"{action.pack()}-{curr_state.get_board()}"


                if key not in self.visited:
                    self.visited.add(key)
                    self.parent[key] = value
                    self.queue.append(action_state)

    def reconstruct_path(self, goal_state):
        path = []
        curr = goal_state

        while curr is not None:
            path.append(curr)
            curr_key = str(curr.get_board())
            curr = self.parent.get(curr_key, None)

        path.reverse()
        return path
