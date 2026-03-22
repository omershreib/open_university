from typing import List
from introduction_to_AI.models import to_vector, Problem
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tiles_models import TileMovement, TILES_ACTIONS
import numpy as np


class TilesGameProblem(Problem):
    def __init__(self, initial_state: TilesGameState, transition_model=None):
        super().__init__()
        self.empty_pos_value = 0
        self.initial_state: TilesGameState = initial_state
        self.actions = TILES_ACTIONS
        self.transition_model = transition_model
        self.goal_state = self._goal_state()
        #self.action_cost = action_cost
        self.game_state: TilesGameState = initial_state

    @property
    def initial_state(self) -> TilesGameState:
        return self._initial_state

    @property
    def game_state(self) -> TilesGameState:
        return self._game_state

    @initial_state.setter
    def initial_state(self, value: TilesGameState):
        print("set initial game state")
        self._initial_state = value

    @game_state.setter
    def game_state(self, value: TilesGameState):
        print("update game state")
        self._game_state = value

    def get_actions(self, state: TilesGameState) -> List[TileMovement]:
        board: np.array = state.get_board()
        blank_pos = to_vector(*np.argwhere(board == self.empty_pos_value)[0])
        valid_actions = []

        for action in self.actions:
            tile_pos: np.array = blank_pos + action
            opp_action_vector = (-1) * action
            tile_movement = TileMovement(None, tile_pos, opp_action_vector)
            if not (tile_movement.is_legal_pos() and tile_movement.is_legal_move()):
                continue

            tile_value = board[*tile_pos]
            tile_movement.value = tile_value
            tile_movement = TileMovement(tile_value, tile_pos, opp_action_vector)
            valid_actions.append(tile_movement)

        return valid_actions

    def is_goal_state(self, state):
        return self._is_boards_equal(state.get_board(), self._goal_state())
        #return np.array_equal(state.get_board(), self._goal_state())
        # return state.get_board() == self._goal_state()

    def update(self, state: TilesGameState, action: TileMovement) -> TilesGameState:
        # print(f"apply movement: {action.describe()}")

        curr_board_state = state.get_tiles_board()
        # equivalent to:
        #   tile_pos, tile_action = tile_movement.pack()
        #   board.move_tile(tile_pos, tile_action)
        action = action.pack()
        new_board_state = curr_board_state.move_tile(*action)
        return TilesGameState(state=new_board_state, parent=curr_board_state, action=action, path_cost=1)

    def _get_tiles_neighbors_to_empty_cell(self):
        current_state_grid = self.game_state.state
        empty_cell_position = np.argwhere(current_state_grid == self.empty_pos_value)
        empty_x = empty_cell_position[0][0]
        empty_y = empty_cell_position[0][1]

        legal_actions: list = []

        for action in self.actions:
            action_x = action[0]
            action_y = action[1]

            tile_x = action_x + empty_x
            tile_y = action_y + empty_y
            tile = (tile_x, tile_y)

            if self._is_legal_tile(tile):
                legal_actions.append(tile)

    @staticmethod
    def _is_legal_tile(tile):
        tile_x, tile_y = tile

        return 0 <= tile_x < 3 and 0 <= tile_y < 3

    @staticmethod
    def _goal_state():
        return np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    @staticmethod
    def _is_boards_equal(board1: np.array, board2: np.array) -> bool:
        return np.array_equal(board1, board2)