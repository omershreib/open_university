from __future__ import annotations

import numpy as np

from introduction_to_AI.agents import DeterministicAgent
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tiles_models import TilesGameProblem, TileMovement, TilesBoard
from collections import deque
from pprint import pprint


class BFSAgent(DeterministicAgent):
    def __init__(self, problem: TilesGameProblem):
        self.problem = problem
        self.visited = set()
        self.queue = deque()
        self.parent = {}
        self.init_board = None

    def init_queue_with_start_state(self, start_state):
        print("add start state into queue")
        self.init_board = start_state.get_board()
        self.queue.append(start_state)
        self.visited.add(start_state)


    def choose_move(self, state):
        actions, path = self.run_bfs(state)
        for action in actions:
            yield action


    def run_bfs(self, state: TilesGameState):
        get_key = lambda x: str(x)
        self.init_queue_with_start_state(state)

        while self.queue:
            curr_state = self.queue.popleft()

            if self.problem.is_goal_state(curr_state):
                return self.reconstruct_actions_path(self.init_board, curr_state.get_board())

            tiles_actions = self.problem.get_actions(curr_state)
            for tile_movement in tiles_actions:
                child_state = self.problem.update(curr_state, tile_movement)
                # child_state.get_tiles_board().display()
                key = get_key(child_state.get_board())
                value = {'tile_movement': tile_movement, 'parent_board': curr_state.get_board()}

                if key not in self.visited:
                    self.visited.add(key)
                    self.parent[key] = value
                    self.queue.append(child_state)

        # in case of no solution
        return None



    def reconstruct_actions_path(self, init_board, goal_board):
        is_board_equals = lambda b1, b2: np.array_equal(b1,b2)
        tile_movements = []
        path = [goal_board]
        curr_board = goal_board

        while not is_board_equals(path[-1], init_board):
            #print(self.parent[str(path[-1])])
            parent_items = self.parent[str(curr_board)]
            tile_movement = parent_items['tile_movement']
            curr_board = parent_items['parent_board']

            #print(f"tile-movement: {tile_movement.describe()}")
            TilesBoard(board=curr_board).display()
            #reversed_action = (-1) * tile_movement.action
            #reversed_tile_movement = TileMovement()
            tile_movements.append(tile_movement)
            path.append(curr_board)

        tile_movements.reverse()
        path.reverse()

        return tile_movements, path
