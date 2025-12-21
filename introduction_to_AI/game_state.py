from __future__ import annotations
from typing import Optional, Tuple, List
from models import ColorDiscPlayer, Move
from bitboard import PlayerBitBoard, legal_moves_mask, apply_move, get_free_bitmask, bits_iter
from bitboard_calculator import BitBoardCalculator


class GameState(BitBoardCalculator):
    def __init__(self, red_bitboard: Optional[PlayerBitBoard], white_bitboard: Optional[PlayerBitBoard],
                 player_turn: Optional[ColorDiscPlayer], board_size: int = 8, consecutive_passes: int = 0):

        super().__init__(board_size)
        self.red_bitboard = red_bitboard
        self.white_bitboard = white_bitboard
        self.board_size = board_size
        self.player_turn = player_turn
        self.consecutive_passes = consecutive_passes

    def initial(self) -> GameState:
        self.red_bitboard = PlayerBitBoard(player=ColorDiscPlayer.RED, board_size=self.board_size)
        self.white_bitboard = PlayerBitBoard(player=ColorDiscPlayer.WHITE, board_size=self.board_size)
        self.red_bitboard.initial()
        self.white_bitboard.initial()

        return GameState(
            red_bitboard=self.red_bitboard,
            white_bitboard=self.white_bitboard,
            board_size=self.board_size,
            player_turn=ColorDiscPlayer.RED,
            consecutive_passes=0
        )

    def set_state(self, red_bits: List[int], white_bits: List[int], player_turn: ColorDiscPlayer) -> GameState:
        self.red_bitboard = PlayerBitBoard(player=ColorDiscPlayer.RED, board_size=self.board_size)
        self.white_bitboard = PlayerBitBoard(player=ColorDiscPlayer.WHITE, board_size=self.board_size)

        for bit in red_bits:
            self.red_bitboard.add_bit(bit)

        for bit in white_bits:
            self.white_bitboard.add_bit(bit)

        return GameState(
            red_bitboard=self.red_bitboard,
            white_bitboard=self.white_bitboard,
            board_size=self.board_size,
            player_turn=player_turn,
            consecutive_passes=0
        )

    def get_players_current_state(self) -> Tuple[PlayerBitBoard, PlayerBitBoard]:
        return (self.red_bitboard, self.white_bitboard) \
            if self.player_turn == ColorDiscPlayer.RED \
            else (self.white_bitboard, self.red_bitboard)

    def legal_moves(self) -> List[Optional[int]]:
        player, opponent = self.get_players_current_state()
        mask = legal_moves_mask(player, opponent)
        if mask == 0:
            return [None]  # PASS
        return list(bits_iter(mask))  # list of single-bit moves

    def actions(self) -> List[Move]:
        actions = []
        for bit in self.legal_moves():
            if bit:
                row, column = self.bit2cell(bit)
                actions.append(Move(row, column))

        return actions

    def update(self, move: Move) -> GameState:
        move_bit = None if move.is_pass else self.cell2bit(move.get_move())
        return self.result(move_bit)

    def result(self, move_bit: Optional[int]) -> GameState:
        player, opponent = self.get_players_current_state()
        updated_player_bitboard, updated_opponent_bitboard = apply_move(player, opponent, move_bit)

        if self.player_turn == ColorDiscPlayer.RED:
            updated_red = updated_player_bitboard
            updated_white = updated_opponent_bitboard
        else:
            updated_red = updated_opponent_bitboard
            updated_white = updated_player_bitboard

        updated_passes = self.consecutive_passes + 1 if move_bit is None else 0

        return GameState(
            red_bitboard=updated_red,
            white_bitboard=updated_white,
            board_size=self.board_size,
            player_turn=self.player_turn.opponent(),
            consecutive_passes=updated_passes
        )

    def is_terminal(self) -> bool:
        # terminal if two consecutive passes OR board full
        if self.consecutive_passes >= 2:
            return True

        #print(f"free: {get_free_bitmask(self.red_bitboard, self.white_bitboard).bit_count()}")
        return get_free_bitmask(self.red_bitboard, self.white_bitboard).bit_count() == 0

    def score(self, player: ColorDiscPlayer) -> int:
        return self.red_bitboard.count() if player == ColorDiscPlayer.RED else self.white_bitboard.count()

    def utility(self, player: ColorDiscPlayer) -> int:
        return self.score(player) - self.score(player.opponent())



