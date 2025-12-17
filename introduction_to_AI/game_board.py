from __future__ import annotations
from typing import Optional, List, Tuple
from models import ColorDiscPlayer, Move

DIRECTIONS: list[tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]


class ReversiGameBoard:
    """Reversi Game Board

    this class maintains this game board.
    board cells can be either empty (None), RED or WHITE
    """

    def __init__(self, board_size: int = 8, grid: Optional[List[List[Optional[ColorDiscPlayer]]]] = None):
        """
        
        :param board_size: even positive integer (by default the size is the classic 8x8 grid)
        :param grid: a 2D array list that represent a snapshot of the game
        """
        self.board_size = board_size
        if grid is None:
            self.grid = [[None for _ in range(board_size)] for _ in range(board_size)]
        else:
            self.grid = grid

    def is_legal_cell(self, cell):
        if not self.is_in_boundaries(cell):
            return False

        return True

    def get_player_cell(self, row: int, column: int) -> Optional[ColorDiscPlayer]:
        return self.grid[row][column]

    def copy(self) -> ReversiGameBoard:
        return ReversiGameBoard(self.board_size, [row[:] for row in self.grid])

    def is_in_boundaries(self, cell) -> bool:
        row, column = cell
        return 0 <= row < self.board_size and 0 <= column < self.board_size

    def initial_game_setup(self) -> ReversiGameBoard:
        """
        Standard Reversi setup:
        RED on left-to-right diagonal center.
        WHITE on right-to-left diagonal center.
        """
        board = self.copy()
        mid = self.board_size // 2
        board.grid[mid - 1][mid - 1] = ColorDiscPlayer.RED
        board.grid[mid][mid] = ColorDiscPlayer.RED
        board.grid[mid - 1][mid] = ColorDiscPlayer.WHITE
        board.grid[mid][mid - 1] = ColorDiscPlayer.WHITE
        return board

    def calc_score(self, player: ColorDiscPlayer) -> int:
        return sum(1 for row in range(self.board_size)
                   for column in range(self.board_size)
                   if self.get_player_cell(row, column) == player)

    def count_empty_cells(self) -> int:
        return sum(1 for row in range(self.board_size)
                   for column in range(self.board_size)
                   if self.get_player_cell(row, column) is None)

    def is_legal_flipping_cell(self, player: ColorDiscPlayer, cell: Tuple[int, int]) -> bool:
        row, column = cell

        if not self.is_in_boundaries(cell):
            return False

        if not self.get_player_cell(row, column) == player.opposition():
            return False

        return True

    def _flips(self, player: ColorDiscPlayer, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """flip opposition player's disc according to player's movement"""
        row, column = cell
        if self.get_player_cell(row, column) is not None:
            return []

        flips: List[Tuple[int, int]] = []

        for vertical_direction, horizontal_direction in DIRECTIONS:

            path: List[Tuple[int, int]] = []
            flip_row = row + vertical_direction
            flip_column = column + horizontal_direction
            flipping_cell = (flip_row, flip_column)

            while self.is_legal_flipping_cell(player, flipping_cell):
                path.append(flipping_cell)
                flip_row += vertical_direction
                flip_column += horizontal_direction
                flipping_cell = (flip_row, flip_column)

            if path and self.is_in_boundaries(flipping_cell) and self.get_player_cell(flip_row, flip_column) == player:
                flips.extend(path)

        return flips

    def legal_moves(self, player: ColorDiscPlayer, include_pass: bool = True) -> List[Move]:
        board_range = range(self.board_size)
        moves: List[Move] = []
        for row in board_range:
            for column in board_range:
                cell = (row, column)
                flips = self._flips(player, cell)

                if self.get_player_cell(row, column) is None and flips:
                    moves.append(Move(row, column))

        if not moves and include_pass:
            return [Move.pass_move()]

        return moves

    def apply_move(self, player: ColorDiscPlayer, move: Move) -> ReversiGameBoard:
        if move.is_pass:
            return self.copy()

        row, column = move.row, move.column
        assert row is not None and column is not None, \
            f"non-pass movement cannot be vertically {row} or horizontally {column} None"

        cell = (row, column)
        flips = self._flips(player, cell)
        if not flips:
            raise ValueError(f"illegal move {move} for {player}")

        board = self.copy()
        board.grid[row][column] = player
        for flip_row, flip_column in flips:
            board.grid[flip_row][flip_column] = player

        return board

    def __str__(self) -> str:
        board_range = range(self.board_size)
        lines = ["  " + " ".join(str(i) for i in board_range)]
        for row in board_range:
            players_discs: list = []
            for column in board_range:
                player = self.get_player_cell(row, column)
                players_discs.append("." if player is None else str(player))
            lines.append(f"{row} " + " ".join(players_discs))
        return "\n".join(lines)
