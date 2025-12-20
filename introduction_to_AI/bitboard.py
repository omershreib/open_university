from __future__ import annotations
from typing import Optional, Tuple, Iterable
from models import ColorDiscPlayer
from bitboard_calculator import BitBoardCalculator


class PlayerBitBoard(BitBoardCalculator):
    def __init__(self, player: ColorDiscPlayer, board_size: int = 8, bitboard: int = 0):

        super().__init__(board_size)

        self.player = player
        self.board_size = board_size
        self.bitboard = bitboard

    def initial(self):
        """initiates player's n x n Reversi bitboard"""
        initial_cells = []

        if self.player == ColorDiscPlayer.RED:
            mid = self.board_size // 2
            initial_cells = [(mid - 1, mid - 1), (mid, mid)]

        if self.player == ColorDiscPlayer.WHITE:
            mid = self.board_size // 2
            initial_cells = [(mid - 1, mid), (mid, mid - 1)]

        self.add_bits_from_cells(initial_cells)

    def disc_color(self):
        return self.player

    def add_bits_from_cells(self, cells):
        for cell in cells:
            self.bitboard |= self.cell2bit(cell)

    def count(self) -> int:
        return (self.bitboard & self.full).bit_count()

    def is_bit_on(self, bit: int) -> bool:
        return (self.bitboard & bit) != 0

    def add_bit(self, bit: int) -> None:
        bitboard = self.bitboard
        self.bitboard = (bitboard | bit) & self.full

    def remove_bit(self, bit: int) -> None:
        bitboard = self.bitboard
        self.bitboard = (bitboard & ~bit) & self.full

    # def union(self, other: "PlayerBitBoard") -> int:
    #     """Return int mask of combined occupancy (still just a mask)."""
    #     return (self.bits | other.bits) & FULL
    #
    # def to_bits(self) -> int:
    #     return self.bits & FULL


def bits_iter(bitboard: int) -> Iterable[int]:
    """Iterate single-bit masks for each set bit in bb.

    this function relies on a very nice two-complement fact, explained as follows:
    let's have `x` a binary number, than:
        x + (-x) = x + (~x + 1) = 0

    where the `~` is the binary NOT operation

    clever conclusion: the LSB of a binary number can be masked by:
        x & (-x)

    for these how slept during this lesson, the way we convert 5 to -5
    (or any number, just for example) in binary representation we need to:
        1. swap all bits, so:
            ~(5) = ~(0000 0101) = 1111 1010

        2. add +1 to the previous result, so:
            1111 1010 + 1 = 1111 1011 = -5


    """
    while bitboard:
        lsb = bitboard & -bitboard
        yield lsb

        # clear this LSB on bitboard by the XOR operation (donated by `^` in python)
        bitboard ^= lsb


def get_occupied_bitmask(player: PlayerBitBoard, opponent: PlayerBitBoard) -> int:
    return (player.bitboard | opponent.bitboard) & player.full


def get_free_bitmask(player: PlayerBitBoard, opponent: PlayerBitBoard) -> int:
    return (~get_occupied_bitmask(player, opponent)) & player.full


def legal_moves_mask(player: PlayerBitBoard, opponent: PlayerBitBoard) -> int:
    """
    Return a bitmask of legal move squares for `player` given `opponent`.

    player's move is considered legal if it obeys free conditions:
        1. (trivial) it is insides the board's boundaries
        2. (trivial) it is not being already performed by one of the players
        3.           it causes for at least a single opponent disc flip under the game's rules
    """
    full = player.full
    player_bitmask = player.bitboard & full
    opponent_bitmask = opponent.bitboard & full
    free_bitmask = (~(player_bitmask | opponent_bitmask)) & full

    moves_mask = 0
    for shift_f in player.all_possible_shifts():
        possible_move = shift_f(player_bitmask) & opponent_bitmask  # opponent adjacent to player in this direction

        while possible_move:
            moves_mask |= shift_f(possible_move) & free_bitmask  # empty square after chain => legal move
            possible_move = shift_f(possible_move) & opponent_bitmask  # extend the chain

    return moves_mask & full


def flips_for_move(player: PlayerBitBoard, opponent: PlayerBitBoard, move_bit: int) -> int:
    """
    Return bitmask of opponent discs flipped if player plays move_bit.
    Assumes move_bit is a FREE single-bit mask
    """
    full = player.full
    player_bitmask = player.bitboard & full
    opponent_bitmask = opponent.bitboard & full
    flips = 0

    for shift_f in player.all_possible_shifts():
        shifted_move = shift_f(move_bit) & opponent_bitmask
        captured = 0

        # while shifted-move is located on opponent's disc needed to be flipped
        # capture this shifted-move (with all the previous captured shifted-moves)
        # stop capturing when arriving player's disc
        while shifted_move:
            captured |= shifted_move
            shifted_move = shift_f(shifted_move)

            if shifted_move & player_bitmask:
                flips |= captured
                break

            shifted_move &= opponent_bitmask

    return flips & full


def apply_move(player: PlayerBitBoard, opponent: PlayerBitBoard, move_bit: Optional[int]) -> Tuple[
    PlayerBitBoard, PlayerBitBoard]:
    """
    Apply a move for `player` vs `opponent`.
    Returns (new_player, new_opponent).
    move_bit=None means PASS (no change).
    """
    if move_bit is None:
        return player, opponent

    occupied_bitmask = get_occupied_bitmask(player, opponent)
    if move_bit & occupied_bitmask:
        raise ValueError("Move on occupied square")

    legal = legal_moves_mask(player, opponent)
    if (move_bit & legal) == 0:
        raise ValueError("Illegal move")

    flips = flips_for_move(player, opponent, move_bit)

    updated_player_bitboard = PlayerBitBoard(
        player=player.disc_color(),
        board_size=player.board_size,
        bitboard=(player.bitboard | move_bit | flips) & player.full
    )

    updated_opponent_bitboard = PlayerBitBoard(
        player=opponent.disc_color(),
        board_size=player.board_size,
        bitboard=(opponent.bitboard & ~flips) & opponent.full
    )

    return updated_player_bitboard, updated_opponent_bitboard
