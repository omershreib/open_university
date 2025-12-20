from __future__ import annotations
from typing import Tuple, List, Optional, Callable
import math


class BitBoardCalculator:
    def __init__(self, board_size: int = 8):
        self.board_size = board_size
        self.square = board_size ** 2

        # bitboard constant bit-masking variables
        self.full: Optional[int] = None  # all bitboard bits are ON
        self.left_edge: Optional[int] = None  # only left-edge column bits are ON
        self.right_edge: Optional[int] = None  # only right-edge column bits are ON
        self.not_left_edge: Optional[int] = None  # only left-edge column bits are OFF
        self.not_right_edge: Optional[int] = None  # only right-edge column bits are OFF

        self._set_bitboard_constants()

    def _set_bitboard_constants(self):
        n = self.board_size
        square = self.square

        # set full-bitboard constant
        self.full = (1 << square) - 1

        # set left-edge bitboard constant
        self.left_edge = sum(1 << (n * row) for row in range(n))

        # set right-edge bitboard constant
        self.right_edge = sum(1 << (n * row + (n - 1)) for row in range(n))

        # set negative (not) left-edge bitboard constant (^ is the XOR operation)
        self.not_left_edge = self.left_edge ^ self.full

        # set negative (not) right-edge bitboard constant
        self.not_right_edge = self.right_edge ^ self.full

    def bit2index(self, bit: int) -> float:
        return math.log(bit, 2)

    def cell2index(self, cell: Tuple[int, int]) -> float:
        return self.bit2index(self.cell2bit(cell))

    def cell2bit(self, cell: Tuple[int, int]) -> int:
        row, column = cell
        return 1 << (self.board_size * row + column)

    def bit2cell(self, bit: int) -> Tuple[int, int]:
        bit_length = bit.bit_length() - 1
        row = bit_length // self.board_size
        column = bit_length % self.board_size
        return row, column

    def shift_up(self, bit: int) -> int:
        """(r, c) -> (r-1, c)"""
        return (bit >> self.board_size) & self.full

    def shift_down(self, bit: int) -> int:
        """(r, c) -> (r+1, c)"""
        return (bit << self.board_size) & self.full

    def shift_left(self, bit: int) -> int:
        """(r, c) -> (r, c-1)"""
        return ((bit & self.not_left_edge) >> 1) & self.full

    def shift_right(self, bit: int) -> int:
        """(r, c) -> (r, c+1)"""
        return ((bit & self.not_right_edge) << 1) & self.full

    def shift_up_left(self, bit: int) -> int:
        """(r, c) -> (r-1, c-1)"""
        return ((bit & self.not_left_edge) >> (self.board_size + 1)) & self.full

    def shift_up_right(self, bit: int) -> int:
        """(r, c) -> (r-1, c+1)"""
        return ((bit & self.not_right_edge) >> (self.board_size - 1)) & self.full

    def shift_down_left(self, bit: int) -> int:
        """(r, c) -> (r+1, c-1)"""
        return ((bit & self.not_left_edge) << (self.board_size - 1)) & self.full

    def shift_down_right(self, bit: int) -> int:
        """(r, c) -> (r+1, c+1)"""
        return ((bit & self.not_right_edge) << (self.board_size + 1)) & self.full

    def all_possible_shifts(self) -> List[Callable[[int], int]]:
        return [self.shift_up,
                self.shift_down,
                self.shift_left,
                self.shift_right,
                self.shift_up_left,
                self.shift_up_right,
                self.shift_down_left,
                self.shift_down_right]
