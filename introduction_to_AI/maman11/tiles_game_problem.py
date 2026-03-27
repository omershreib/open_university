from typing import List, Optional
from introduction_to_AI.common import vector
from introduction_to_AI.models.problem import Problem
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tile_movement import TileMovement, TILES_DIRECTIONS
import numpy as np


class TilesGameProblem(Problem):
    """Tiles Game Formalized Problem Class Suit"""

    def __init__(self, initial_state: TilesGameState):
        """

        :param initial_state: a TilesGameState initial state
        """
        super().__init__()

        self.empty_pos_value = 0
        self.initial_state: TilesGameState = initial_state
        n = self.__size = initial_state.size
        self.goal_state: TilesGameState = TilesGameState(board=self.create_goal_board(n), size=n)
        self.directions = TILES_DIRECTIONS
        self.game_state: TilesGameState = initial_state

    @property
    def initial_state(self) -> TilesGameState:
        return self._initial_state

    @property
    def game_state(self) -> TilesGameState:
        return self._game_state

    @initial_state.setter
    def initial_state(self, value: Optional[TilesGameState]):
        self._initial_state = value

        if isinstance(value, TilesGameState):
            self._initial_state.depth = 0

    @game_state.setter
    def game_state(self, value: TilesGameState):
        self._game_state = value

    @property
    def goal_state(self):
        return self._goal_state

    @goal_state.setter
    def goal_state(self, goal_state_config):
        self._goal_state = goal_state_config

    def get_actions(self, state: TilesGameState) -> List[TileMovement]:
        board: np.array = state.board
        bound = state.size
        blank_pos = vector(*np.argwhere(board == self.empty_pos_value)[0])
        valid_actions = []

        for direction in self.directions:
            tile_pos: np.array = blank_pos + direction
            opp_action_vector = (-1) * direction
            tile_movement = TileMovement(None, tile_pos, opp_action_vector, bound=bound)
            if not (tile_movement.is_legal_pos() and tile_movement.is_legal_move()):
                continue

            tile_value = board[*tile_pos]
            tile_movement.value = tile_value
            tile_movement = TileMovement(tile_value, tile_pos, opp_action_vector)
            valid_actions.append(tile_movement)

        return valid_actions

    def is_goal_state(self, state):
        return self._is_boards_equal(state.board, self.goal_state.board)

    def update(self, state: TilesGameState, action: TileMovement) -> TilesGameState:
        packed_action = action.pack()
        moved_state = state.move_tile(*packed_action)
        size = state.size

        return TilesGameState(board=moved_state.board, size=size)

    def args_action(self, curr_state: TilesGameState, next_state: TilesGameState):
        curr_board = curr_state.board
        next_board = next_state.board
        curr_empty_pos = np.argwhere(curr_board == 0)[0]
        next_empty_pos = np.argwhere(next_board == 0)[0]

        # The moved tile is the one that moved into the old empty position.
        tile_pos = next_empty_pos
        tile_value = curr_board[tuple(tile_pos)]

        direction = curr_empty_pos - next_empty_pos

        return TileMovement(
            tile_value=tile_value,
            tile_pos=tile_pos,
            direction=direction
        )

    def action_cost(self, curr_state, action, result_state):
        return 1

    @staticmethod
    def create_goal_board(n: int):
        """
        Create an n x n goal board for the tiles game.

        Example:
            n=3 -> [[0,1,2],[3,4,5],[6,7,8]]
            n=4 -> [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]
        """
        return [[i * n + j for j in range(n)] for i in range(n)]


    @staticmethod
    def _is_legal_tile(tile):
        tile_x, tile_y = tile

        return 0 <= tile_x < 3 and 0 <= tile_y < 3

    @staticmethod
    def _is_boards_equal(board1: np.array, board2: np.array) -> bool:
        return np.array_equal(board1, board2)
