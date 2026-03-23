from __future__ import annotations

from introduction_to_AI.agents import BFSAgent, ManhattanAgent
from introduction_to_AI.models import make_node, expand
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tiles_game_problem import TilesGameProblem
from introduction_to_AI.maman11.tiles_models import TileMovement
from introduction_to_AI.maman11.tiles_evaluators import TilesManhattanEvaluator
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



class TilesManhattanAgent(ManhattanAgent):
    def __init__(self, problem, goal_state, evaluator=None):
        #self.curr_state: TilesGameState = kwargs.get('curr_state')
        self.goal_state: TilesGameState = goal_state
        self.problem = problem
        self.evaluator = TilesManhattanEvaluator(problem=self.problem)

        super().__init__(problem=problem, goal_state=goal_state, evaluator=self.evaluate)


    def evaluate(self, state):
        return self.evaluator.evaluate(curr_state=state, goal_state=self.goal_state)





