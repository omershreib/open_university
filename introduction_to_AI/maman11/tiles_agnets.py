from __future__ import annotations

from introduction_to_AI.agents import BFSAgent
from introduction_to_AI.models import make_node, expand
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tiles_game_problem import TilesGameProblem
from introduction_to_AI.maman11.tiles_models import TileMovement
from collections import deque
import numpy as np


class TilesBFSAgent(BFSAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def build_actions_plan(self, state):
        goal_node, path = self.run(state)
        actions = self.reconstruct_actions_path(path)
        return actions

    def reconstruct_actions_path(self, path):
        """
        Convert a path of states into a list of TileMovement objects.

        Args:
            path: list of game states from start to goal

        Returns:
            list[TileMovement]
        """
        if not path or len(path) < 2:
            return []

        actions = []

        for i in range(len(path) - 1):
            curr_board = path[i].get_board()
            next_board = path[i + 1].get_board()

            movement = self._infer_tile_movement(curr_board, next_board)
            actions.append(movement)

        return actions

    def _infer_tile_movement(self, curr_board, next_board):
        """
        Infer the tile movement between two consecutive boards.
        Assumes 0 is the empty tile.
        """
        curr_empty_pos = np.argwhere(curr_board == 0)[0]
        next_empty_pos = np.argwhere(next_board == 0)[0]

        # The moved tile is the one that moved into the old empty position.
        tile_pos = next_empty_pos
        tile_value = curr_board[tuple(tile_pos)]

        action = curr_empty_pos - next_empty_pos

        return TileMovement(
            tile_value=tile_value,
            tile_pos=tile_pos,
            action=action
        )

# class BFSAgent(DeterministicAgent, TilesGameProblem):
#     def __init__(self, init_state: TilesGameState):
#         DeterministicAgent.__init__(self, 'BFS')
#         TilesGameProblem.__init__(self, init_state)
#         self.visited = set()
#         self.queue = deque()
#         self.parent = {}
#         self.init_board = None
#         self.expanded_nodes = 0
#
#     def init_queue_with_start_state(self, start_state):
#         print("reset agent attibutes")
#         self.visited = set()
#         self.queue = deque()
#         self.parent = {}
#         self.expanded_nodes = 0
#
#         print("add start state into queue")
#         self.init_board = start_state.get_board()
#         self.queue.append(start_state)
#         self.visited.add(self.get_key(start_state.get_board()))
#         #self.visited.add(start_state)
#
#     def build_actions_plan(self, state):
#         actions, path = self.run_bfs(state)
#         for action in actions:
#             yield action
#
#     def gpt_run_bfs(self, state: TilesGameState):
#         self.init_queue_with_start_state(state)
#
#
#         while self.queue:
#             curr_state = self.queue.popleft()
#
#             if self.is_goal_state(curr_state):
#                 return self.reconstruct_actions_path(self.init_board, curr_state.get_board())
#
#             self.expanded_nodes += 1
#
#             curr_node = make_node(state=curr_state)
#
#             for child_node in expand(self, curr_node):
#                 child_state = child_node.state
#                 child_key = self.get_key(child_state.get_board())
#
#                 if child_key in self.visited:
#                     continue
#
#                 self.visited.add(child_key)
#                 self.parent[child_key] = child_node
#
#                 # if self.is_goal_state(child_state):
#                 #     return self.reconstruct_actions_path(
#                 #         self.init_board,
#                 #         child_state.get_board()
#                 #     )
#
#                 self.queue.append(child_state)
#
#         return None
#
#     def run_bfs(self, state: TilesGameState):
#         self.init_queue_with_start_state(state)
#
#         if self.is_goal_state(state):
#             return self.reconstruct_actions_path(self.init_board, self.init_board)
#
#         while self.queue:
#             curr_state = self.queue.popleft()
#
#             # increase number of expanded nodes
#             self.expanded_nodes += 1
#
#             for child in expand(self, make_node(state=curr_state)):
#                 child_state = child.state
#                 key = self.get_key(child_state.get_board())
#
#                 if key not in self.visited:
#                     self.visited.add(key)
#                     self.parent[key] = child
#
#                     if self.is_goal_state(child_state):
#                         return self.reconstruct_actions_path(self.init_board, child_state.get_board())
#
#                     self.queue.append(child_state)
#
#         # in case of no solution
#         return None
#
#     def reconstruct_actions_path(self, init_board, goal_board):
#         tile_movements = []
#         path = [goal_board]
#         curr_board = goal_board
#
#         while not self._is_boards_equal(path[-1], init_board):
#             # parent_items = self.parent[self.get_key(curr_board)]
#             # tile_movement = parent_items['tile_movement']
#             # curr_board = parent_items['parent_board']
#             parent_state = self.parent[self.get_key(curr_board)].state
#             tile_pos, tile_action = parent_state.action
#             tile_movement = TileMovement(tile_value=None,tile_pos=tile_pos, action=tile_action)
#             # TilesBoard(board=curr_board).display()
#             tile_movements.append(tile_movement)
#             curr_board = parent_state.parent.board
#             path.append(curr_board)
#
#         tile_movements.reverse()
#         path.reverse()
#
#         return tile_movements, path
