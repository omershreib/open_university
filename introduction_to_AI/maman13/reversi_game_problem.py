from __future__ import annotations

from typing import List
from introduction_to_AI.models import Problem

from introduction_to_AI.maman13.bitboard import PlayerBitBoard
from .reversi_cdp import ColorDiskPlayer
from .reversi_move import ReversiMove
from .reversi_game_state import ReversiGameState


class ReversiGameProblem(Problem):
    def __init__(self,
                 max_player: ColorDiskPlayer = ColorDiskPlayer.RED,
                 min_player: ColorDiskPlayer = ColorDiskPlayer.WHITE,
                 size: int = 8):

        super().__init__()

        self.initial_state: ReversiGameState = self.__initial(size)
        self.players = {'maximum': max_player, 'minimum': min_player}

        # self.goal_state = { list of all terminals ReversiGameState }

        self.game_state: ReversiGameState = self.initial_state

    @property
    def initial_state(self) -> ReversiGameState:
        return self._initial_state

    @initial_state.getter
    def initial_state(self):
        return self._initial_state

    @initial_state.setter
    def initial_state(self, value: ReversiGameState):
        self._initial_state = value

    def __initial(self, size) -> ReversiGameState:
        self.red_bitboard = PlayerBitBoard(player=ColorDiskPlayer.RED, board_size=size)
        self.white_bitboard = PlayerBitBoard(player=ColorDiskPlayer.WHITE, board_size=size)
        self.red_bitboard.initial()
        self.white_bitboard.initial()

        print(self.red_bitboard.bitboard)
        print(self.white_bitboard.bitboard)

        return ReversiGameState(
            red_bitboard=self.red_bitboard,
            white_bitboard=self.white_bitboard,
            board_size=size,
            player_turn=ColorDiskPlayer.RED,
            consecutive_passes=0
        )

    def get_actions(self, state: ReversiGameState) -> List[ReversiMove]:
        actions = []
        for bit in state.legal_moves():
            if bit:
                row, column = state.bit2cell(bit)
                actions.append(ReversiMove(row, column))

        return actions

    def update(self, state: ReversiGameState, move: ReversiMove) -> ReversiGameState:
        move_bit = None if move.is_pass else state.cell2bit(move.get_move())
        return state.result(move_bit, move)

    def is_goal_state(self, state: ReversiGameState):
        return state.is_terminal()

    def action_cost(self, curr_state, action, result_state):
        return 1

    def args_action(self, state) -> ReversiMove:
        return state.move_creator
