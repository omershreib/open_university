from __future__ import annotations

from typing import Optional, Tuple, List
from introduction_to_AI.models import State
from introduction_to_AI.maman13.bitboard import (PlayerBitBoard,
                                                 legal_moves_mask,
                                                 apply_move,
                                                 get_free_bitmask,
                                                 bits_iter)

from introduction_to_AI.maman13.bitboard_calculator import BitBoardCalculator
from introduction_to_AI.maman13.reversi_cdp import ColorDiskPlayer
from introduction_to_AI.maman13.reversi_move import ReversiMove


class ReversiGameState(State, BitBoardCalculator):
    def __init__(self,
                 red_bitboard: Optional[PlayerBitBoard] = None,
                 white_bitboard: Optional[PlayerBitBoard] = None,
                 player_turn: Optional[ColorDiskPlayer] = None,
                 board_size: int = 8,
                 consecutive_passes: int = 0,
                 move_creator: Optional[ReversiMove] = None):

        super().__init__(board_size)
        self.red_bitboard = red_bitboard
        self.white_bitboard = white_bitboard
        self.board_size = board_size
        self.player_turn = player_turn
        self.consecutive_passes = consecutive_passes
        self.move_creator = move_creator

    def get_key(self):
        pass

    def get_value(self):
        pass

    def display(self):
        pass

    def initial(self, size) -> ReversiGameState:
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

    def check_cell(self, cell: Tuple[int, int]) -> Optional[ColorDiskPlayer]:
        """

        check which player occupies cell (row, column).
        if cell is empty, return None
        """
        bit = self.cell2bit(cell)

        if self.red_bitboard.is_bit_on(bit):
            return ColorDiskPlayer.RED

        if self.white_bitboard.is_bit_on(bit):
            return ColorDiskPlayer.WHITE

        return None

    def snapshot(self):
        board_range = range(self.board_size)
        lines = ["  " + " ".join(str(i) for i in board_range)]
        for row in board_range:
            players_discs: list = []
            for column in board_range:
                player = self.check_cell((row, column))
                players_discs.append("." if player is None else str(player))
            lines.append(f"{row} " + " ".join(players_discs))

        return "\n".join(lines)

    # def set_state(self, red_bits: List[int],
    #               white_bits: List[int],
    #               player_turn: ColorDiskPlayer) -> ReversiGameState:
    #
    #     self.red_bitboard = PlayerBitBoard(player=ColorDiskPlayer.RED, board_size=self.board_size)
    #     self.white_bitboard = PlayerBitBoard(player=ColorDiskPlayer.WHITE, board_size=self.board_size)
    #
    #     for bit in red_bits:
    #         self.red_bitboard.add_bit(bit)
    #
    #     for bit in white_bits:
    #         self.white_bitboard.add_bit(bit)
    #
    #     return ReversiGameState(
    #         red_bitboard=self.red_bitboard,
    #         white_bitboard=self.white_bitboard,
    #         board_size=self.board_size,
    #         player_turn=player_turn,
    #         consecutive_passes=0
    #     )

    def legal_moves(self) -> List[Optional[int]]:
        player, opponent = self.get_players_current_state()
        mask = legal_moves_mask(player, opponent)
        if mask == 0:
            return [None]  # PASS
        return list(bits_iter(mask))  # list of single-bit moves

    def result(self, move_bit: Optional[int], move: ReversiMove) -> ReversiGameState:
        player, opponent = self.get_players_current_state()
        updated_player_bitboard, updated_opponent_bitboard = apply_move(player, opponent, move_bit)

        if self.player_turn == ColorDiskPlayer.RED:
            updated_red = updated_player_bitboard
            updated_white = updated_opponent_bitboard
        else:
            updated_red = updated_opponent_bitboard
            updated_white = updated_player_bitboard

        updated_passes = self.consecutive_passes + 1 if move_bit is None else 0

        return ReversiGameState(
            red_bitboard=updated_red,
            white_bitboard=updated_white,
            board_size=self.board_size,
            player_turn=self.player_turn.opponent(),
            consecutive_passes=updated_passes,
            move_creator=move
        )

    def get_players_current_state(self) -> Tuple[PlayerBitBoard, PlayerBitBoard]:
        return (self.red_bitboard, self.white_bitboard) \
            if self.player_turn == ColorDiskPlayer.RED \
            else (self.white_bitboard, self.red_bitboard)

    def is_terminal(self) -> bool:
        # terminal if two consecutive passes OR board full
        if self.consecutive_passes >= 2:
            return True

        return get_free_bitmask(self.red_bitboard, self.white_bitboard).bit_count() == 0

    def score(self, player: ColorDiskPlayer) -> int:
        return self.red_bitboard.count() if player == ColorDiskPlayer.RED else self.white_bitboard.count()

    def utility(self, player: ColorDiskPlayer) -> int:
        return self.score(player) - self.score(player.opponent())

    def __repr__(self):
        return f"<ReversiGameState: {self.get_key()}>"


if __name__ == '__main__':
    #player = ColorDiskPlayer.RED
    #print(player == ColorDiskPlayer.RED)

    #player_bitboard = PlayerBitBoard(player=ColorDiskPlayer.RED, board_size=8)
    #print(player_bitboard.player)
    #print(player_bitboard.player == ColorDiskPlayer.RED)

    state = ReversiGameState().initial(size=8)
    print(state.snapshot())
